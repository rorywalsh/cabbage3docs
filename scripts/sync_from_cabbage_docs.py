#!/usr/bin/env python3
"""
Sync documentation from cabbage-docs (Astro/Starlight, the single source of
truth) into cabbage3site (Docusaurus).

Run from anywhere (paths are resolved from the script's own location):

    python3 scripts/sync_from_cabbage_docs.py [--dry-run]

Reads, and never writes:

    ../cabbage-docs/src/content/docs/docs/        the doc pages
    ../cabbage-docs/src/components/properties/    the widget property components

Writes:

    docs/                                          the Docusaurus pages
    docs/cabbage_widgets/properties/               the property components

It never touches static/ (the .csd examples and images), blog/, src/ or
sidebars.ts.  The sidebar is hand-maintained: a page with no sidebar entry is
reported at the end so it can be added by hand.

The conversions are:

    frontmatter      title and description are carried over; Astro-only keys
                     (head:, sidebar:) are dropped.
    imports          MDX import lines are dropped; widget pages keep the
                     import header that already exists in the site.
    components       <WidgetExample> is dropped, <ExampleCode> becomes the
                     site's <CodeBlock>, <LinkCard> becomes a bullet link.
    links            /docs/... becomes a relative link to the site page,
                     /install/ becomes the live install page.
    comments         <!-- --> and {/* */} are removed (a .md file would print
                     the latter literally).
    callouts         :::note, :::caution and :::tip are kept: Docusaurus
                     understands them natively.
    properties       the .astro components are rendered back to .mdx.
"""

from __future__ import annotations

import html
import posixpath
import re
import sys
from pathlib import Path

SITE_ROOT = Path(__file__).parent.parent.resolve()
DOCS_ROOT = SITE_ROOT.parent / "cabbage-docs"

DOCS_PAGES = DOCS_ROOT / "src" / "content" / "docs" / "docs"
DOCS_PROPS = DOCS_ROOT / "src" / "components" / "properties"
SITE_PAGES = SITE_ROOT / "docs"
SITE_PROPS = SITE_ROOT / "docs" / "cabbage_widgets" / "properties"

DRY_RUN = "--dry-run" in sys.argv

# docs folder -> site folder
SECTION_MAP = {
    "using": "using_cabbage",
    "widgets": "cabbage_widgets",
    "custom-ui": "custom_interfaces",
    "opcodes": "cabbage_opcodes",
}

# docs file stem -> site file stem, where the names differ
ALIASES = {
    "index": "intro",
    "whats-new": "cabbage3",
    "faqs": "faqs",
    # using/
    "audio-channels": "channels",
    "exporting": "exporting_instruments",
    # custom-ui/
    "js-api": "CabbageJS_API",
}

# used only when a page called "overview" has no match of its own
OVERVIEW_FALLBACK = "intro"

INSTALL_URL = "https://cabbageaudio.com/install/"

warnings: list[str] = []
notes: list[str] = []

# The page being converted, so property components can rewrite links too.
CURRENT: "Page | None" = None


def warn(message: str) -> None:
    warnings.append(message)


def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


# --------------------------------------------------------------------------
# frontmatter
# --------------------------------------------------------------------------


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not match:
        return {}, text
    fields: dict[str, str] = {}
    current: str | None = None
    for line in match.group(1).splitlines():
        if line[:1] in (" ", "\t"):
            continue  # nested block (head:, sidebar:)
        key_value = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if key_value:
            current = key_value.group(1)
            fields[current] = key_value.group(2).strip()
    return fields, text[match.end() :]


def build_frontmatter(title: str, description: str) -> str:
    out = f"---\ntitle: {quote(title)}\n"
    if description:
        out += f"description: {quote(description)}\n"
    return out + "---\n\n"


# --------------------------------------------------------------------------
# code fences: everything inside one is left alone
# --------------------------------------------------------------------------


def split_fences(text: str) -> list[tuple[bool, str]]:
    parts: list[tuple[bool, str]] = []
    buffer: list[str] = []
    marker: str | None = None

    def flush(is_code: bool) -> None:
        if buffer:
            # The newline that followed this part's last line belonged to the
            # split, not to the line: keep it so prose and the fence below it
            # do not end up on one line.
            parts.append((is_code, "\n".join(buffer) + "\n"))
            buffer.clear()

    for line in text.split("\n"):
        opening = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if marker is None:
            if opening:
                flush(False)
                marker = opening.group(1)[0] * 3
                buffer.append(line)
            else:
                buffer.append(line)
        else:
            buffer.append(line)
            if (
                opening
                and opening.group(1)[0] == marker[0]
                and len(opening.group(1)) >= 3
                and not opening.group(2).strip()
            ):
                flush(True)
                marker = None
    flush(marker is not None)
    return parts


# --------------------------------------------------------------------------
# link rewriting
# --------------------------------------------------------------------------


class Page:
    """One page being converted: knows where it lands on the site."""

    def __init__(
        self,
        docs_rel: str,
        site_rel: str,
        page_index: dict[str, str],
        site_dir: str | None = None,
    ):
        self.docs_rel = docs_rel
        self.site_rel = site_rel
        self.page_index = page_index
        self.site_dir = site_dir if site_dir is not None else posixpath.dirname(site_rel)

    def site_path_for(self, docs_rel: str) -> str | None:
        return self.page_index.get(normalize(docs_rel))

    def relative_link(self, site_rel: str) -> str:
        without_ext = re.sub(r"\.(md|mdx)$", "", site_rel)
        rel = posixpath.relpath(without_ext, self.site_dir or ".")
        if not rel.startswith("."):
            rel = "./" + rel
        return rel

    def rewrite(self, target: str) -> str:
        fragment = ""
        if "#" in target:
            target, fragment = target.split("#", 1)
            fragment = "#" + fragment

        if re.match(r"^(https?:|mailto:)", target):
            return target + fragment
        if target in ("/install", "/install/"):
            return INSTALL_URL + fragment
        if not target.startswith("/docs"):
            if target.startswith("/"):
                warn(f"{self.site_rel}: unhandled link {target}")
            return target + fragment

        rest = target[5:].strip("/")
        parts = [part for part in rest.split("/") if part]
        key = normalize("".join(parts)) if parts else normalize("index")
        site_rel = self.page_index.get(key)
        if site_rel is None:
            warn(f"{self.site_rel}: no site page for link {target}")
            return target + fragment
        return self.relative_link(site_rel) + fragment


def build_page_index() -> tuple[dict[str, str], list[str]]:
    """Map every docs page (keyed by its normalised path) to its site path."""
    index: dict[str, str] = {}
    missing: list[str] = []
    site_files_by_dir: dict[str, dict[str, str]] = {}

    for folder in SECTION_MAP.values():
        directory = SITE_PAGES / folder
        site_files_by_dir[folder] = {}
        if directory.is_dir():
            for path in sorted(directory.iterdir()):
                if path.suffix in (".md", ".mdx"):
                    site_files_by_dir[folder][normalize(path.stem)] = path.name

    for docs_path in sorted(DOCS_PAGES.rglob("*")):
        if docs_path.suffix not in (".md", ".mdx") or not docs_path.is_file():
            continue
        docs_rel = str(docs_path.relative_to(DOCS_PAGES))
        stem = docs_path.stem
        section = docs_path.parent.name

        if section == "docs":  # a root page
            target = SITE_PAGES / (ALIASES.get(stem, stem) + docs_path.suffix)
        elif section in SECTION_MAP:
            folder = SECTION_MAP[section]
            folder_files = site_files_by_dir.get(folder, {})
            name = folder_files.get(normalize(stem))
            if name is None and stem in ALIASES:
                name = folder_files.get(normalize(ALIASES[stem]))
            if name is None and stem == "overview":
                name = folder_files.get(normalize(OVERVIEW_FALLBACK))
            if name is None:
                missing.append(docs_rel)
                continue
            target = SITE_PAGES / folder / name
        else:
            missing.append(docs_rel)
            continue

        index[normalize(docs_rel[: -len(docs_path.suffix)])] = str(
            target.relative_to(SITE_ROOT)
        )
    return index, missing


# --------------------------------------------------------------------------
# page body conversion
# --------------------------------------------------------------------------


def site_import_header(site_rel: str) -> list[str]:
    path = SITE_ROOT / site_rel
    if not path.is_file():
        return []
    header = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("import "):
            header.append(line)
        elif header:
            break
    return header


def find_example(name: str) -> str | None:
    """The example file the docs page asks for, matched without case."""
    wanted = SITE_ROOT / "static" / "examples" / f"{name}.csd"
    if wanted.is_file():
        return wanted.name
    for candidate in sorted((SITE_ROOT / "static" / "examples").glob("*.csd")):
        if candidate.stem.lower() == name.lower():
            return candidate.name
    return None


def example_variable(header: list[str], name: str) -> str | None:
    """Which raw-loader variable on this page holds the named example?"""
    first = None
    for line in header:
        match = re.match(
            r"import\s+(\w+)\s+from\s+'!!raw-loader!.*?static/examples/([^']+)'", line
        )
        if not match:
            continue
        first = first or match.group(1)
        if match.group(2).lower() == f"{name}.csd".lower():
            return match.group(1)
    return first


def point_header_at(header: list[str], name: str, site_rel: str) -> list[str]:
    """Make the page's raw-loader import read the example the docs page names.

    The example files themselves are not touched: only the import path in the
    page changes, and only when the file the docs ask for already exists in
    static/examples.
    """
    found = find_example(name)
    if found is None:
        warn(f"{site_rel}: static/examples/{name}.csd does not exist; example kept as is")
        return header
    wanted = f"static/examples/{found}"
    if any(wanted in line for line in header):
        return header
    fixed = []
    done = False
    for line in header:
        if not done and "!!raw-loader!" in line and "static/examples/" in line:
            line = re.sub(r"static/examples/[^']+", wanted, line)
            done = True
        fixed.append(line)
    if not done:
        fixed.append(f"import widgetCode from '!!raw-loader!../../{wanted}';")
    return fixed


def convert_link_cards(text: str, page: Page) -> str:
    def card(match: re.Match[str]) -> str:
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', match.group(0)))
        title = attrs.get("title", "")
        description = attrs.get("description", "")
        href = page.rewrite(attrs.get("href", ""))
        line = f"- [**{title}**]({href})"
        if description:
            line += f" — {description}"
        return line

    text = re.sub(r"[ \t]*<LinkCard\b.*?/>", card, text, flags=re.S)
    text = re.sub(r"[ \t]*</?CardGrid>", "", text)
    return text


def convert_widget_components(text: str, page: Page, header: list[str]) -> str:
    text = re.sub(r"<WidgetExample\b.*?/>", "", text, flags=re.S)

    def example_code(match: re.Match[str]) -> str:
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', match.group(0)))
        name = attrs.get("name", "")
        variable = example_variable(header, name)
        if variable is None:
            warn(f"{page.site_rel}: no example file for <ExampleCode name=\"{name}\">")
            return ""
        return f'<CodeBlock language="csound">{{{variable}}}</CodeBlock>'

    return re.sub(r"<ExampleCode\b.*?/>", example_code, text, flags=re.S)


def transform_body(body: str, page: Page, header: list[str]) -> tuple[str, list[str]]:
    """Fence-aware pass: comments, imports, components and links."""
    out: list[str] = []
    for is_code, chunk in split_fences(body):
        if is_code:
            out.append(chunk)
            continue
        chunk = re.sub(r"<!--.*?-->", "", chunk, flags=re.S)
        chunk = re.sub(r"\{/\*.*?\*/\}", "", chunk, flags=re.S)
        chunk = re.sub(r"^import\s+[^\n]*\n", "", chunk, flags=re.M)
        chunk = convert_link_cards(chunk, page)
        chunk = convert_widget_components(chunk, page, header)
        chunk = re.sub(r"\]\(([^)\s]+)\)", lambda m: "](" + page.rewrite(m.group(1)) + ")", chunk)
        out.append(chunk)
    return "".join(out), out


def dead_example_import(line: str, body: str) -> bool:
    if "!!raw-loader!" not in line:
        return False
    match = re.match(r"import\s+(\w+)", line)
    return match is not None and match.group(1) not in body


def component_names(text: str) -> set[str]:
    """Components used in prose, ignoring code fences and inline code spans."""
    names = set()
    for is_code, chunk in split_fences(text):
        if is_code:
            continue
        chunk = re.sub(r"`[^`]*`", "", chunk)
        names.update(re.findall(r"<([A-Z][A-Za-z0-9]*)\b[^>]*>", chunk))
    return names


def property_imports() -> dict[str, str]:
    """Component variable -> property file, read from every site widget page."""
    mapping: dict[str, str] = {}
    widget_dir = SITE_PAGES / SECTION_MAP["widgets"]
    for path in sorted(widget_dir.glob("*.md*")):
        for line in path.read_text(encoding="utf-8").splitlines():
            match = re.match(r'import\s+(\w+)\s+from\s+"(\./properties/[^"]+)"', line)
            if match:
                mapping[match.group(1)] = match.group(2)
    return mapping


def convert_page(
    docs_path: Path, site_rel: str, page: Page, known: dict[str, str], is_widget: bool
) -> str:
    fields, body = split_frontmatter(docs_path.read_text(encoding="utf-8"))
    title = unquote(fields.get("title", "")) or docs_path.stem.replace("-", " ").title()
    description = unquote(fields.get("description", ""))

    header = site_import_header(site_rel) if is_widget else []
    # The docs pages keep a TODO inside a comment that names the components a
    # page will need one day; comments are dropped, so they must not be read.
    without_comments = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    without_comments = re.sub(r"\{/\*.*?\*/\}", "", without_comments, flags=re.S)
    for name in re.findall(r'<ExampleCode\b[^>]*name="([^"]*)"', without_comments):
        header = point_header_at(header, name, site_rel)
    body, _ = transform_body(body, page, header)

    # An example the docs page no longer shows leaves a dead import behind.
    header = [line for line in header if not dead_example_import(line, body)]

    used = component_names(body)
    imported = {re.match(r"import\s+(\w+)", line).group(1) for line in header if re.match(r"import\s+(\w+)", line)}
    added = []
    for name in sorted(used - imported - {"CodeBlock"}):
        path = known.get(name)
        if path is None:
            warn(f"{site_rel}: <{name} /> is not a known component; left unconverted")
            continue
        added.append(f'import {name} from "{path}";')
        header = header + added[-1:]

    out = build_frontmatter(title, description)
    if header:
        out += "\n".join(header) + "\n\n"
    out += body.strip() + "\n"
    return out


# --------------------------------------------------------------------------
# property components (.astro -> .mdx)
# --------------------------------------------------------------------------


def unescape_literal(value: str) -> str:
    return re.sub(r"\\(.)", r"\1", value)


def extract_codes(body: str) -> tuple[str, list[dict[str, str]]]:
    codes: list[dict[str, str]] = []
    out: list[str] = []
    position = 0
    while True:
        opening = re.search(r"<Code\b", body[position:])
        if not opening:
            break
        start = position + opening.start()
        code_at = body.find("code={`", start)
        if code_at == -1:
            break
        index = code_at + len("code={`")
        cursor = index
        while cursor < len(body):
            if body[cursor] == "\\":
                cursor += 2
                continue
            if body[cursor] == "`":
                break
            cursor += 1
        literal = body[index:cursor]
        lang_match = re.search(r'lang="([\w-]+)"', body[cursor : cursor + 400])
        lang = lang_match.group(1) if lang_match else "text"
        tag_end = body.find("/>", cursor + (lang_match.end() if lang_match else 0))
        if tag_end == -1:
            break
        tag_end += 2
        codes.append({"lang": lang, "code": unescape_literal(literal).strip()})
        out.append(body[position:start])
        out.append(f"\x00{len(codes) - 1}\x00")
        position = tag_end
    out.append(body[position:])
    return "".join(out), codes


def restore_codes(text: str, codes: list[dict[str, str]]) -> str:
    def restore(match: re.Match[str]) -> str:
        code = codes[int(match.group(1))]
        return f"```{code['lang']}\n{code['code']}\n```"

    return re.sub(r"\x00(\d+)\x00", restore, text)


def inline_markdown(text: str) -> str:
    text = re.sub(
        r"<code>(.*?)</code>",
        lambda m: "`" + re.sub(r"\s+", " ", m.group(1)).strip() + "`",
        text,
        flags=re.S,
    )
    text = re.sub(r"<strong>(.*?)</strong>", r"**\1**", text, flags=re.S)
    text = re.sub(r"<em>(.*?)</em>", r"*\1*", text, flags=re.S)
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(
        r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>',
        lambda m: "[{}]({})".format(
            re.sub(r"\s+", " ", m.group(2)).strip(),
            CURRENT.rewrite(m.group(1)) if CURRENT else m.group(1),
        ),
        text,
        flags=re.S,
    )
    return html.unescape(text)


def table_to_markdown(table: str) -> str:
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", table, flags=re.S)
    lines = []
    for row_index, row in enumerate(rows):
        cells = re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", row, flags=re.S)
        cells = [inline_markdown(re.sub(r"\s+", " ", cell)).strip() for cell in cells]
        lines.append("| " + " | ".join(cells) + " |")
        if row_index == 0:
            lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
    return "\n\n" + "\n".join(lines) + "\n\n"


def html_to_markdown(text: str) -> str:
    def callout(match: re.Match[str]) -> str:
        attrs, inner = match.group(1), match.group(2)
        kind = re.search(r'type="(\w+)"', attrs)
        title = re.search(r'title="([^"]*)"', attrs)
        heading = f":::{kind.group(1) if kind else 'note'}"
        if title:
            heading += " " + title.group(1)
        inner_md = html_to_markdown(inner).strip()
        return f"\n\n{heading}\n{inner_md}\n:::\n\n"

    text = re.sub(r"<Callout([^>]*)>(.*?)</Callout>", callout, text, flags=re.S)

    def blockquote(match: re.Match[str]) -> str:
        inner = html_to_markdown(match.group(1)).strip()
        lines = ["> " + line if line else ">" for line in inner.split("\n")]
        return "\n\n" + "\n".join(lines) + "\n\n"

    text = re.sub(r"<blockquote>(.*?)</blockquote>", blockquote, text, flags=re.S)
    text = re.sub(
        r"<table[^>]*>.*?</table>",
        lambda match: table_to_markdown(match.group(0)),
        text,
        flags=re.S,
    )

    def unordered_list(match: re.Match[str]) -> str:
        items = re.findall(r"<li[^>]*>(.*?)</li>", match.group(1), flags=re.S)
        lines = [
            "- " + inline_markdown(re.sub(r"\s+", " ", item)).strip() for item in items
        ]
        return "\n\n" + "\n".join(lines) + "\n\n"

    text = re.sub(r"<ul[^>]*>(.*?)</ul>", unordered_list, text, flags=re.S)
    text = re.sub(r"<p[^>]*>", "\n\n", text)
    text = text.replace("</p>", "\n\n")
    text = re.sub(r"</?div[^>]*>", "\n", text)
    text = inline_markdown(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    # The source HTML is indented inside the .astro component; left as it is,
    # those four spaces would turn every paragraph into a code block.
    text = re.sub(r"^[ \t]+", "", text, flags=re.M)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def convert_property(astro_path: Path, page_index: dict[str, str]) -> str:
    raw = astro_path.read_text(encoding="utf-8")
    _, body = split_frontmatter(raw)

    global CURRENT
    previous = CURRENT
    site_rel = str((SITE_PROPS / (astro_path.stem + ".mdx")).relative_to(SITE_ROOT))
    # A property component is inlined into a widget page, so its links have to
    # resolve from that page, one level up from properties/.
    CURRENT = Page(site_rel, site_rel, page_index, site_dir=posixpath.dirname(site_rel.replace("/properties/", "/")))

    description_match = re.search(r"const description = `(.*?)`;", raw, re.S)
    if description_match:
        body = re.sub(
            r"<Fragment\s+set:html=\{description\}\s*/>", description_match.group(1), body
        )

    body, codes = extract_codes(body)
    body = html_to_markdown(body)
    body = re.sub(
        r"\]\(([^)\s]+)\)",
        lambda match: "](" + CURRENT.rewrite(match.group(1)) + ")",
        body,
    )
    body = restore_codes(body, codes)
    body = re.sub(r"\n{3,}", "\n\n", body)
    CURRENT = previous
    leftover = set(re.findall(r"</?(?:div|p|ul|li|table|tr|td|th|a|strong|code)\b", body))
    if leftover:
        warn(f"{astro_path.name}: unconverted markup {sorted(leftover)}")
    return body.strip() + "\n"


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------


def write(path: Path, content: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.is_file() else None
    if old == content:
        return False
    notes.append(f"wrote {path.relative_to(SITE_ROOT)}")
    if not DRY_RUN:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


def main() -> int:
    if not DOCS_PAGES.is_dir():
        print(f"error: {DOCS_ROOT} does not hold the docs source")
        return 1

    page_index, missing = build_page_index()
    for rel in missing:
        print(f"error: no site page for docs/{rel} (add the file or the sidebar entry)")
    if missing:
        return 1

    known = property_imports()
    changed = 0
    total = 0

    # ---- doc pages -------------------------------------------------------
    for docs_path in sorted(DOCS_PAGES.rglob("*")):
        if docs_path.suffix not in (".md", ".mdx") or not docs_path.is_file():
            continue
        docs_rel = str(docs_path.relative_to(DOCS_PAGES))
        without_ext = docs_rel[: -len(docs_path.suffix)]
        site_rel = page_index.get(normalize(without_ext))
        if site_rel is None:
            continue
        total += 1
        page = Page(docs_rel, site_rel, page_index)
        is_widget = docs_path.parent.name == "widgets"
        content = convert_page(docs_path, site_rel, page, known, is_widget)
        if write(SITE_ROOT / site_rel, content):
            changed += 1

    # ---- property components --------------------------------------------
    props_changed = 0
    props_total = 0
    for astro_path in sorted(DOCS_PROPS.glob("*.astro")):
        props_total += 1
        target = SITE_PROPS / (astro_path.stem + ".mdx")
        if write(target, convert_property(astro_path, page_index)):
            props_changed += 1

    for orphan in sorted(SITE_PROPS.glob("*.mdx")):
        if not (DOCS_PROPS / (orphan.stem + ".astro")).exists():
            print(f"note: {orphan.relative_to(SITE_ROOT)} has no docs source")

    # ---- report ----------------------------------------------------------
    print(f"pages:   {changed} of {total} written")
    print(f"props:   {props_changed} of {props_total} written")
    for message in notes:
        print(f"  {message}")
    for message in warnings:
        print(f"  warning: {message}")
    if DRY_RUN:
        print("(dry run: nothing was written)")
    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())

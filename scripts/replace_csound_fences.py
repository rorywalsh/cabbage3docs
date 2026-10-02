#!/usr/bin/env python3
"""
Replace all occurrences of ```csound with ```json in files under a path.

Usage:
  python3 replace_csound_fences.py /path/to/docs [--extensions mdx md]

By default this operates in-place and only on `.mdx` and `.md` files.
Use `--dry-run` to print which files would be changed without writing.
"""
import argparse
from pathlib import Path
import sys


def process_file(path: Path, dry: bool) -> int:
    try:
        s = path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"[error] cannot read {path}: {e}")
        return 0

    count = s.count("```csound")
    if count == 0:
        return 0

    new = s.replace("```csound", "```json")
    if not dry:
        try:
            path.write_text(new, encoding='utf-8')
        except Exception as e:
            print(f"[error] cannot write {path}: {e}")
            return 0
        print(f"Updated: {path} ({count} replacements)")
    else:
        print(f"Would update: {path} ({count} replacements)")

    return count


def main():
    p = argparse.ArgumentParser()
    p.add_argument('root', nargs='?', default='.', help='Root folder to search')
    p.add_argument('--extensions', '-e', nargs='+', default=['mdx','md'], help='File extensions to process')
    p.add_argument('--dry-run', action='store_true', help='Do not write files')
    args = p.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.exists():
        print(f"Path not found: {root}")
        sys.exit(2)

    exts = set('.' + e.lstrip('.') for e in args.extensions)

    total_files = 0
    total_replacements = 0

    for path in root.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in exts:
            continue
        total_files += 1
        total_replacements += process_file(path, args.dry_run)

    print(f"\nScanned {total_files} files; made {total_replacements} total replacements")


if __name__ == '__main__':
    main()

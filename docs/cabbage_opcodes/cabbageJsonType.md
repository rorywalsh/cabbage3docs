import CodeBlock from '@theme/CodeBlock';
import jsonCode from '!!raw-loader!../../static/examples/cabbageJson.csd';

# cabbageJsonType

This opcode reports the JSON type of the value at a dot-notation path, so the orchestra can branch before querying. It is the typesafe companion to [cabbageJsonGet](./cabbageJsonGet): use it when an empty string or zero is ambiguous (missing vs. present-but-empty, `"123"` vs. `123`).

## Syntax
```csound
type:S = cabbageJsonType(json:S, path:S)
```

### Initialization
* *json:S* – a string holding a valid JSON document
* *path:S* – dot-notation path into the document, where numeric segments index arrays
* *type:S* – one of `"string"`, `"number"`, `"boolean"`, `"array"`, `"object"`, `"null"`, or `"missing"` (invalid documents report `"missing"` for every path)

### Performance
* Works at k-rate; the document is re-parsed only when the input text changes

## Example:

```csound
instr 1
    doc:S = "{\"freq\":\"440\"}"
    type:S = cabbageJsonType(doc, "freq")
    if strcmp(type, "string") == 0 then
        prints("frequency arrived as text, parsing...\n")
    endif
    freq:k = cabbageJsonGet(doc, "freq")
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

<CodeBlock language="csound">{jsonCode}</CodeBlock>

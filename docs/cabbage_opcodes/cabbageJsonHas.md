import CodeBlock from '@theme/CodeBlock';
import jsonCode from '!!raw-loader!../../static/examples/cabbageJson.csd';

# cabbageJsonHas

This opcode checks whether a dot-notation path exists in a JSON document (`nodes.0.params.rate`, where numeric segments index arrays). Unlike a query that returns an empty value, it distinguishes "missing" from "present but null/zero". See also [cabbageJsonType](./cabbageJsonType) and [cabbageJsonGet](./cabbageJsonGet).

## Syntax
```csound
has:i = cabbageJsonHas(json:S, path:S)
has:k = cabbageJsonHas(json:S, path:S)
```

### Initialization
* *json:S* – a string holding a valid JSON document
* *path:S* – dot-notation path into the document
* *has:i* – `1` when the path exists (even if its value is `null`), else `0`

### Performance
* *has:k* – as *has:i*, re-evaluated each k-cycle

## Example:

```csound
instr 1
    doc:S = "{\"params\":{\"rate\":2.5}}"
    if cabbageJsonHas(doc, "params.rate") == 1 then
        rate:k = cabbageJsonGet(doc, "params.rate")
    endif
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

<CodeBlock language="csound">{jsonCode}</CodeBlock>

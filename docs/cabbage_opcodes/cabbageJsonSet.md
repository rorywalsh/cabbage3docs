import CodeBlock from '@theme/CodeBlock';
import jsonCode from '!!raw-loader!../../static/examples/cabbageJson.csd';

# cabbageJsonSet

This opcode returns a new JSON document with the value at a dot-notation path replaced (`nodes.0.params.rate`, where numeric segments index arrays). Intermediate objects are created as needed. Array elements can be replaced by index; setting out of range, or through a type clash, leaves the output empty and logs a warning. Query the result with [cabbageJsonGet](./cabbageJsonGet).

## Syntax
```csound
json:S = cabbageJsonSet(json:S, path:S, val:S)
json:S = cabbageJsonSet(json:S, path:S, val:k)
```

### Initialization
* *json:S* – a string holding a valid JSON document
* *path:S* – dot-notation path to set
* *val:S/val:k* – the new value (string or number)
* Returns the updated document as a string, or `""` on failure

### Performance
* Works at k-rate

## Example:

```csound
instr 1
    doc:S = "{\"params\":{\"rate\":2.5}}"
    doc = cabbageJsonSet(doc, "params.rate", 4)
    doc = cabbageJsonSet(doc, "params.wave", "sine")
    rate:k = cabbageJsonGet(doc, "params.rate")
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

<CodeBlock language="csound">{jsonCode}</CodeBlock>

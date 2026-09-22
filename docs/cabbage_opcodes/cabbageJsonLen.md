import CodeBlock from '@theme/CodeBlock';
import jsonCode from '!!raw-loader!../../static/examples/cabbageJson.csd';

# cabbageJsonLen

This opcode returns the size of the value at a dot-notation path in a JSON document: array length or object key count. Missing paths, scalars, and invalid documents yield `0`. See also [cabbageJsonGet](./cabbageJsonGet) and [cabbageJsonHas](./cabbageJsonHas).

## Syntax
```csound
len:i = cabbageJsonLen(json:S, path:S)
len:k = cabbageJsonLen(json:S, path:S)
```

### Initialization
* *json:S* – a string holding a valid JSON document
* *path:S* – dot-notation path into the document (`nodes.0.params`, where numeric segments index arrays)
* *len:i* – number of elements/keys, or `0`

### Performance
* *len:k* – as *len:i*, re-evaluated each k-cycle

## Example:

```csound
instr 1
    doc:S = "{\"gains\":[1, 2.5, 3]}"
    arr:k[] = cabbageJsonGet(doc, "gains")
    n:i = lenarray(arr)
    printf("mixing %d channels\n", 1, n)
endin
```

## Full example

The following instrument exercises the JSON opcodes against a patcher-style state document:

<CodeBlock language="csound">{jsonCode}</CodeBlock>

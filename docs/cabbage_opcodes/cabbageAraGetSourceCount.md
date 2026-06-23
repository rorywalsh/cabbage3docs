# cabbageAraGetSourceCount

Returns the total number of ARA audio sources currently available in the shared ARA document model.

## Syntax
```csound
iCount cabbageAraGetSourceCount
kCount cabbageAraGetSourceCount
```

### Initialization
* *iCount* — number of valid ARA sources

### Performance
* *kCount* — number of valid ARA sources (updated each k-cycle)

## Description

In ARA, all plugin instances in a project share one document model that can contain many audio sources (e.g., across multiple tracks). This opcode returns how many sources are currently present. Use this value to iterate over sources and query their metadata using opcodes like `cabbageAraGetSourceName`, `cabbageAraGetSourceChannels`, etc.

## Example

```csound
instr 1
  iCount cabbageAraGetSourceCount
  prints("Number of sources: %d\n", iCount)
endin
```

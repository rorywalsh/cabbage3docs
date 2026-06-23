# cabbageAraGetSourceName

Returns the name of an ARA audio source by index.

## Syntax
```csound
SName cabbageAraGetSourceName iIndex
```

### Initialization
* *iIndex* — zero-based source index
* *SName* — name of the source (empty string if index is out of range)

## Description

Returns the name string for the audio source at the given index in the ARA document model. Prints a warning if the index is out of range.

## Example

```csound
instr 1
  iCount cabbageAraGetSourceCount
  idx = 0
  while idx < iCount do
    SName cabbageAraGetSourceName idx
    prints("Source %d: %s\n", idx, SName)
    idx += 1
  od
endin
```

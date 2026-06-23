# cabbageAraGetSourceSr

Returns the sample rate for an ARA source by index.

## Syntax
```csound
iSr cabbageAraGetSourceSr iIndex
kSr cabbageAraGetSourceSr kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iSr* — sample rate in Hz

### Performance
* *kIndex* — zero-based source index
* *kSr* — sample rate in Hz

## Description

Returns the sample rate (e.g., 44100, 48000) for the ARA source at the given index. Prints a warning if the index is out of range.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iSr cabbageAraGetSourceSr iIndex
  prints("Source %d sample rate: %d\n", iIndex, iSr)
endin
```

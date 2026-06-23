# cabbageAraGetSourceSampleCount

Returns the total number of samples for an ARA source by index.

## Syntax
```csound
iSamples cabbageAraGetSourceSampleCount iIndex
kSamples cabbageAraGetSourceSampleCount kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iSamples* — total sample count

### Performance
* *kIndex* — zero-based source index
* *kSamples* — total sample count

## Description

Returns the total number of audio samples for the ARA source at the given index. Prints a warning if the index is out of range.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iSamples cabbageAraGetSourceSampleCount iIndex
  prints("Source %d has %d samples\n", iIndex, iSamples)
endin
```

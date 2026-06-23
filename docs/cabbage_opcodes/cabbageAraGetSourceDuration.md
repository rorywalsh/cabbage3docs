# cabbageAraGetSourceDuration

Returns the duration in seconds for an ARA source by index.

## Syntax
```csound
iDur cabbageAraGetSourceDuration iIndex
kDur cabbageAraGetSourceDuration kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iDur* — duration in seconds

### Performance
* *kIndex* — zero-based source index
* *kDur* — duration in seconds

## Description

Returns the duration in seconds for the ARA source at the given index. Computed as `sampleCount / sampleRate`. Prints a warning if the index is out of range or sample rate is zero.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iDur cabbageAraGetSourceDuration iIndex
  prints("Source %d duration: %.2f seconds\n", iIndex, iDur)
endin
```

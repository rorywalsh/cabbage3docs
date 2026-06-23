# cabbageAraGetRegionSampleCount

Returns the number of samples in the playback region for an ARA source.

## Syntax
```csound
iCount cabbageAraGetRegionSampleCount iIndex
kCount cabbageAraGetRegionSampleCount kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iCount* — region sample count

### Performance
* *kIndex* — zero-based source index
* *kCount* — region sample count

## Description

Returns the duration of the current playback region in samples for the ARA source at the given index. This is the `regionDuration` value stored in the ARA data pool. Prints a warning if the index is out of range.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iCount cabbageAraGetRegionSampleCount iIndex
  iStart cabbageAraGetRegionSampleStart iIndex
  prints("Region: %d to %d (%d samples)\n", iStart, iStart + iCount - 1, iCount)
endin
```

# cabbageAraGetRegionDuration

Returns the duration of the playback region in seconds for an ARA source.

## Syntax
```csound
iDur cabbageAraGetRegionDuration iIndex
kDur cabbageAraGetRegionDuration kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iDur* — region duration in seconds

### Performance
* *kIndex* — zero-based source index
* *kDur* — region duration in seconds

## Description

Returns the duration of the current playback region in seconds for the ARA source at the given index. Computed as `regionDuration / sampleRate`. Prints a warning if the index is out of range or the sample rate is zero.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iDur cabbageAraGetRegionDuration iIndex
  prints("Region duration: %.2f seconds\n", iDur)
endin
```

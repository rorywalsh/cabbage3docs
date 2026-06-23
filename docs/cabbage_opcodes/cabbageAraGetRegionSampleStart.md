# cabbageAraGetRegionSampleStart

Returns the start sample position of the playback region for an ARA source.

## Syntax
```csound
iStart cabbageAraGetRegionSampleStart iIndex
kStart cabbageAraGetRegionSampleStart kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iStart* — start sample position

### Performance
* *kIndex* — zero-based source index
* *kStart* — start sample position

## Description

Returns the start sample index of the current playback region for the ARA source at the given index. This defines where within the source the host is currently reading from. Prints a warning if the index is out of range.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iStart cabbageAraGetRegionSampleStart iIndex
  prints("Region starts at sample %d\n", iStart)
endin
```

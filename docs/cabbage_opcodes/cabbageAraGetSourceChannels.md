# cabbageAraGetSourceChannels

Returns the number of audio channels for an ARA source by index.

## Syntax
```csound
iChannels cabbageAraGetSourceChannels iIndex
kChannels cabbageAraGetSourceChannels kIndex
```

### Initialization
* *iIndex* — zero-based source index
* *iChannels* — number of channels

### Performance
* *kIndex* — zero-based source index
* *kChannels* — number of channels

## Description

Returns the channel count (e.g., 1 for mono, 2 for stereo) for the ARA source at the given index. Prints a warning if the index is out of range.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iChans cabbageAraGetSourceChannels iIndex
  prints("Source %d has %d channels\n", iIndex, iChans)
endin
```

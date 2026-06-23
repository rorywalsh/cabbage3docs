# cabbageAraGetSourceSamples

Reads PCM audio data from an ARA source. Available in four variants: a-rate (audio output), k-rate (k-rate output), k-array, and i-array.

## Syntax
```csound
aOut cabbageAraGetSourceSamples aPos, iChan, iSourceIndex
kOut cabbageAraGetSourceSamples kPos, iChan, iSourceIndex
kSamples[] cabbageAraGetSourceSamples iStart, iCount, iChan, iSourceIndex
iSamples[] cabbageAraGetSourceSamples iStart, iCount, iChan, iSourceIndex
```

### Initialization
* *iChan* — zero-based channel index within the source
* *iSourceIndex* — zero-based source index
* *iStart* — first sample to read (array variants)
* *iCount* — number of samples to read (array variants)

### Performance
* *aPos* / *kPos* — sample position to read at (per-sample or per-k-cycle)
* *aOut* / *kOut* — output sample value at the given position

### Output arrays
* *kSamples[]* / *iSamples[]* — array of PCM samples from `iStart` to `iStart + iCount - 1`

## Description

This opcode provides direct access to the raw PCM audio data of an ARA source. The a-rate and k-rate variants read a single sample at the position given by `aPos`/`kPos`. The array variants read a contiguous block of samples starting at `iStart` for `iCount` samples.

Sample positions outside the valid range return 0. Prints warnings if the source index, channel index, or PCM data are invalid.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex

  ; Read first 100 samples from channel 0 as an array
  iSamples[] cabbageAraGetSourceSamples 0, 100, 0, iIndex

  ; Or read sample-by-sample at audio rate
  aphase phasor sr
  aOut cabbageAraGetSourceSamples aphase, 0, iIndex
endin
```

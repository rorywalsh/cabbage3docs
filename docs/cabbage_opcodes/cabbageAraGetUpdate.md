# cabbageAraGetUpdate

Returns a monotonic counter that increments whenever ARA model data changes.

## Syntax
```csound
kUpdate cabbageAraGetUpdate
```

### Performance
* *kUpdate* — update counter (k-rate only)

## Description

This opcode returns an integer counter that increments each time the shared ARA document model data is refreshed. Use it as a trigger to re-read source metadata using `cabbageAraGet`. A common pattern is to detect changes with `changed:k()` and launch a reader instrument on change.

## Example

```csound
instr 1
  kUpdate cabbageAraGetUpdate
  kTrig changed kUpdate
  if kTrig == 1 then
    event "i", "ReadAraData", 0, 0.001
  endif
endin

instr ReadAraData
  iIdx  cabbageAraGet "currentIndex"
  iCnt  cabbageAraGet "audioSourceCount"
  SLast cabbageAraGet "lastEvent"
  prints("Update [%s]: source %d of %d\n", SLast, iIdx, iCnt)
endin
```

## See Also

- [cabbageAraGet](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGet)
- [cabbageAraGetSourceSamples](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGetSourceSamples)

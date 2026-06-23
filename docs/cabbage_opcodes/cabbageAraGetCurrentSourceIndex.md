# cabbageAraGetCurrentSourceIndex

Returns the index of the ARA audio source associated with the current plugin instance/track.

## Syntax
```csound
iIndex cabbageAraGetCurrentSourceIndex
kIndex cabbageAraGetCurrentSourceIndex
```

### Initialization
* *iIndex* — index of the current source

### Performance
* *kIndex* — index of the current source (updated each k-cycle)

## Description

Each plugin instance in an ARA project is associated with one audio source. This opcode returns the index of that source, which can be used with opcodes like `cabbageAraGetSourceName` to query source metadata. The index may change during a session as DAW events occur, so it is recommended to use `cabbageAraGetUpdate` as a trigger when reading data.

Returns `-1` if the engine is not available.

## Example

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  prints("Current source index: %d\n", iIndex)
endin
```

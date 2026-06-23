# cabbageAraGetCurrentSourceName

Returns the name of the ARA audio source associated with the current plugin instance/track.

## Syntax
```csound
SName cabbageAraGetCurrentSourceName
```

### Initialization
* *SName* — name of the current source (empty string if unavailable)

## Description

Convenience opcode that returns the name string of the source associated with the current plugin instance. Returns an empty string if the engine is not available or the source cannot be found.

## Example

```csound
instr 1
  SName cabbageAraGetCurrentSourceName
  prints("Current source: %s\n", SName)
endin
```

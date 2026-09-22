---
title: cabbageAraGetStateJson
description: Return the entire ARA state as a JSON string
---

# cabbageAraGetStateJson

Returns the complete ARA data pool as a JSON string. Useful for passing ARA state directly to a web frontend or other JSON consumers.

## Synopsis

```csound
SJson cabbageAraGetStateJson                     ; i-rate: dump once on init
SJson cabbageAraGetStateJson kTrig               ; k-rate: dump on trigger
```

## Description

`cabbageAraGetStateJson` serializes the entire ARA document model state into a JSON string. The JSON contains all sections that `cabbageAraDump` prints in detailed mode, but as a structured string rather than formatted text.

The **i-rate** version returns the JSON once when the instrument initializes.

The **k-rate** version takes a trigger signal and returns a fresh JSON string each time the trigger transitions from zero to nonzero.

### JSON Structure

```json
{
  "currentIndex": 0,
  "update": 12,
  "lastEvent": "notifySelection",
  "sourceCount": 1,
  "sources": [
    {
      "name": "cleanGuitar.wav",
      "channels": 1,
      "sampleRate": 44100,
      "sampleCount": 3226747,
      "duration": 73.169,
      "regionStartInSamples": 0,
      "regionDurationInSamples": 3226747,
      "regionStart": 0.0,
      "regionDuration": 73.169
    }
  ],
  "playbackRegionCount": 1,
  "playbackRegions": [
    {
      "name": "cleanGuitar.wav",
      "regionSequenceName": "cleanGuitar",
      "playbackStart": 0.0,
      "playbackDuration": 73.169,
      "regionStartInSamples": 0,
      "regionDurationInSamples": 3226747,
      "colorR": 0.0,
      "colorG": 0.0,
      "colorB": 1.0
    }
  ],
  "musicalContextCount": 1,
  "musicalContexts": [ ... ],
  "regionSequenceCount": 1,
  "regionSequences": [ ... ],
  "audioModificationCount": 1,
  "audioModifications": [ ... ],
  "editorView": {
    "selectedRegions": [ ... ],
    "hiddenSequenceCount": 0,
    "timeRangeStart": 0.0,
    "timeRangeDuration": 73.169
  }
}
```

## Example

```csound
; Get JSON once at init
instr 1
  SJson cabbageAraGetStateJson
  printks "JSON: %s\n", 1, SJson
endin

; Get JSON on each ARA update
instr 2
  kTrig cabbageAraGetUpdate
  SJson cabbageAraGetStateJson kTrig
endin

; Write JSON to a file for a web frontend
instr 3
  kTrig cabbageAraGetUpdate
  if kTrig > 0 then
    SJson cabbageAraGetStateJson kTrig
    fprintk 2, SJson  ; print to stderr or a file
  endif
endin
```

## See Also

- [cabbageAraDump](/cabbage3docs/docs/cabbage_opcodes/cabbageAraDump)
- [cabbageAraGet](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGet)
- [cabbageAraGetUpdate](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGetUpdate)

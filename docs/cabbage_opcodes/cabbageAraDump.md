---
title: cabbageAraDump
description: Print the entire ARA state to the Csound output for diagnostics
---

# cabbageAraDump

Prints a formatted dump of the entire ARA data pool to the Csound output. Useful for debugging and understanding the state of the ARA document model.

## Synopsis

```csound
cabbageAraDump()                          ; i-rate: dump once on init
cabbageAraDump(kTrig)                    ; k-rate: dump on trigger
```

## Description

`cabbageAraDump` is a diagnostic opcode that prints the complete ARA state to the Csound output window.

The **i-rate** version takes no arguments and dumps once when the instrument initializes.

The **k-rate** version takes a trigger signal and dumps each time the trigger transitions from zero to nonzero.

The output includes:

- **Status**: Last ARA event, update counter
- **Metrics**: Source count, playback region count, selected region count, current source index
- **Time Range**: Host arrangement timeline position
- **Playback Regions**: All clips in the document with their arrangement position and source crop
- **Selected Regions**: Currently selected clips with timeline position and source crop
- **Sources**: All audio sources with channels, sample rate, duration, and region crop

## Example

```csound
; Dump once at init
instr 1
  cabbageAraDump
endin

; Dump on each ARA update
instr 2
  kTrig cabbageAraGetUpdate
  cabbageAraDump kTrig
endin
```

## Output Format

```
=========================================
ARA STATE DUMP
=========================================
[Status]  Last Event:   notifySelection
[Status]  Update:       5
[Metrics] Sources: 2  |  Regions: 5  |  Selected: 2  |  Hidden: 0  |  Current Index: 0
[Time]    Host Range: 1.000 to 3.500 (2.500s)

------------ PLAYBACK REGIONS ------------
[1] 'guitar.wav'
    Start:    1.000s
    Duration: 2.500s
    Source Crop: Start=44100 samples, Dur=110250 samples

------------ SELECTED REGIONS ------------
[1] 'guitar.wav'
    Timeline Pos: 1.000s (Dur: 2.500s)
    Source Crop:  Start=44100 samples, Dur=110250 samples (2.500s)

------------ SOURCES ---------------------
[1] 'guitar.wav'
    Channels:    2
    Sample Rate: 44100 Hz
    Sample Count: 176400
    Duration:    4.000s
    Region:      Start=44100 (1.000s), Duration=110250 (2.500s)
=========================================
```

It is also quite simple to iterate over the global ARA pool manually by accessing the individual ARA properties:

```csound
instr ShowAllInfo
    cabbageAraDump()
    ; --- Top-level state ---
    idx:i      = cabbageAraGet("currentIndex")
    srcCnt:i   = cabbageAraGet("audioSourceCount")
    lastEvent:S = cabbageAraGet("lastEvent")

    ; Print the header block
    printfi("=========================================\n", 1)
    printfi("ARA UPDATE No.%d\n", 1, p5)
    printfi("=========================================\n", 1)
    printfi("[Status]  Last Event:   %s\n", 1, lastEvent)

    ; --- Selection properties ---
    regCnt:i    = cabbageAraGet("playbackRegionCount")
    selRegCnt:i = cabbageAraGet("selectedPlaybackRegionCount")
    printfi("[Metrics] Source Count: %d  |  Region Count: %d  |  Selected: %d  |  Current Index: %d\n", 1, srcCnt, regCnt, selRegCnt, idx)

    ; --- Time Range Calculations ---
    trStart:i = cabbageAraGet("editorView.timeRange.start")
    trDur:i   = cabbageAraGet("editorView.timeRange.duration")
    printfi("[Time]    Host Range:   %.3f to %.3f (%.3fs)\n\n", 1, trStart, trStart + trDur, trDur)

    ; --- Playback Regions Loop ---
    printfi("------------ PLAYBACK REGIONS ------------\n", 1)
    if regCnt == 0 then
        printfi("    [None]\n", 1)
    else
        selIdx:i = 0
        while selIdx < regCnt do
            selName:S    = cabbageAraGet("playbackRegion.name", selIdx)
            pbStart:i    = cabbageAraGet("playbackRegion.start", selIdx)
            pbDur:i      = cabbageAraGet("playbackRegion.duration", selIdx)

            printfi("[%d] '%s'\n", selIdx + 1, selIdx, selName)
            printfi("    Start:    %.3fs\n", 1, pbStart)
            printfi("    Duration: %.3fs\n", 1, pbDur)
            selIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Selected Regions Loop (New Section) ---
    printfi("------------ SELECTED REGIONS ------------\n", 1)
    if selRegCnt == 0 then
        printfi("    [None]\n", 1)
    else
        activeSelIdx:i = 0
        while activeSelIdx < selRegCnt do
            selRegName:S    = cabbageAraGet("playbackRegion.selectedRegionName", activeSelIdx)
            selTimelineStart:i = cabbageAraGet("playbackRegion.selectedPlaybackStart", activeSelIdx)
            selTimelineDur:i   = cabbageAraGet("playbackRegion.selectedPlaybackDuration", activeSelIdx)
            selSrcStartSamp:i  = cabbageAraGet("playbackRegion.selectedRegionStartInSamples", activeSelIdx)
            selSrcDurSamp:i    = cabbageAraGet("playbackRegion.selectedRegionDurationInSamples", activeSelIdx)

            printfi("[%d] '%s'\n", activeSelIdx + 1, activeSelIdx, selRegName)
            printfi("    Timeline Pos: %.3fs (Dur: %.3fs)\n", 1, selTimelineStart, selTimelineDur)
            printfi("    Source Crop:  Start=%d samples, Dur=%d samples\n", 1, selSrcStartSamp, selSrcDurSamp)
            activeSelIdx += 1
        od
    endif
    printfi("\n", 1)

    ; --- Sources Loop ---
    printfi("------------ SOURCES ---------------------\n", 1)
    if srcCnt == 0 then
        printfi("    [None]\n", 1)
    else
        srcIdx:i = 0
        while srcIdx < srcCnt do
            name:S      = cabbageAraGet("audioSource.name", srcIdx)
            channels:i  = cabbageAraGet("audioSource.channels", srcIdx)
            sampCnt:i   = cabbageAraGet("audioSource.sampleCount", srcIdx)
            sr:i        = cabbageAraGet("audioSource.sampleRate", srcIdx)
            duration:i  = cabbageAraGet("audioSource.duration", srcIdx)
            regStart:i  = cabbageAraGet("audioSource.region.startInSamples", srcIdx)
            regDur:i    = cabbageAraGet("audioSource.region.durationInSamples", srcIdx)

            printfi("[%d] '%s'\n", srcIdx + 1, srcIdx, name)
            printfi("    Channels: %d\n", 1, channels)
            printfi("    Sample Rate: %d Hz\n", 1, sr)
            printfi("    Sample Count: %d\n", 1, sampCnt)
            printfi("    Duration: %.3fs\n", 1, duration)
            printfi("    Region: Start=%d, Duration=%d\n", 1, regStart, regDur)
            srcIdx += 1
        od
    endif
    printfi("=========================================\n", 1)

endin
```

## See Also

- [cabbageAraGet](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGet)
- [cabbageAraGetUpdate](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGetUpdate)

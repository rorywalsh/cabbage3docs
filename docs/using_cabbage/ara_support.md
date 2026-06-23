---
title: ARA Support
description: Using ARA (Audio Random Access) with Cabbage 3
---

ARA (Audio Random Access) is an extension to the standard audio plugin format that gives a plugin direct, offline access to a host's audio material — without having to process it in real time. Cabbage supports ARA through a suite of dedicated opcodes that provide access to the host's audio tracks.

### Exporting an ARA plugin

ARA support is only available in dedicated ARA build targets. When exporting your plugin from the Cabbage extension, you must choose one of the ARA-specific export commands:

- **Export as VST3 Effect (ARA)**
- **Export as VST3 Synth (ARA)**

These commands are available from the VS Code Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux). Exporting with a standard VST3 or CLAP target will produce a plugin that does not include ARA support.

### How it works

When an ARA-capable host loads a Cabbage plugin, it grants the plugin direct access to the audio material on each track. Cabbage reads this audio data directly from the host, stores it in an internal data pool, and makes it available to your Csound instrument through a set of ARA opcodes.

All Cabbage ARA plugin instances in a project share one document model. That model can contain many audio sources (for example, across multiple tracks). Cabbage provides opcodes to query source metadata, read audio samples, and detect when the model is updated.

### Querying source metadata

Use the ARA opcodes to query information about the available audio sources:

```csound
instr 1
  sourceCount:i = cabbageAraGetSourceCount()
  sourceIndex:i = cabbageAraGetCurrentSourceIndex()
  sourceName:i = cabbageAraGetCurrentSourceName()
  sourceNumChans:i = cabbageAraGetSourceChannels(sourceIndex)
  sourceNumSamples:i = cabbageAraGetSourceSampleCount(sourceIndex)
  sourceSR:i = cabbageAraGetSourceSr(sourceIndex)
  sourceDuration:i cabbageAraGetSourceDuration(sourceIndex)

  prints("Source '%s': %d channels, %d samples, %d Hz, %.2f sec\n",
         sourceName, sourceNumChans, sourceNumSamples, sourceSR, sourceDuration)
endin
```

### Reading audio data

Use `cabbageAraGetSourceSamples` to read raw PCM data from a source. It supports audio-rate, k-rate, and array output. To read the contents of the track the plugin is currently loaded onto, do this:

```csound
instr 1
  sourceIndex:i = cabbageAraGetCurrentSourceIndex()
  sourceNumSamples:i = cabbageAraGetSourceSampleCount(sourceIndex)
  ; Read samples from channel 0 as a k-rate array
  kSamples[] = cabbageAraGetSourceSamples(0, sourceNumSamples, 0, sourceIndex)

  ; Or read sample-by-sample at audio rate
  phaseIncr = phasor(sr/sourceNumSamples)
  sig:a = cabbageAraGetSourceSamples(aPhase, 0, iIndex)
  out(sig, sig)
endin
```

### Detecting updates

`cabbageAraGetUpdate` returns a counter that increments whenever the ARA model data changes. Use it as a trigger to re-read source metadata. This listener will fire whenever changes are made to the session, for example timeline changes, new clips added, clips resized, etc. 

```csound
instr 1
    updated:k = cabbageAraGetUpdate()
    if changed:k(updated) == 1 then
        event "i", "ReadAraData", 0, 3600
    endif
endin

instr ReadAraData
  numSources:i = cabbageAraGetSourceCount()
  index:i = cabbageAraGetCurrentSourceIndex()
  prints("Update: %d number of sources, current index = %d\n", numSources, index)
endin
```

### Playback regions

ARA hosts define playback regions that specify which portion of a source is active. Use the region opcodes to query these:

```csound
instr 1
  iIndex cabbageAraGetCurrentSourceIndex
  iStart cabbageAraGetRegionSampleStart iIndex
  iCount cabbageAraGetRegionSampleCount iIndex
  iDur cabbageAraGetRegionDuration iIndex

  prints("Region: sample %d, %d samples (%.2f sec)\n", iStart, iCount, iDur)
endin
```

### Testing without a DAW (CabbageApp)

During development, you can test ARA instruments without an ARA-capable host by using CabbageApp's standalone mode. When the VS Code extension launches a standalone ARA instrument, it will prompt you to select an audio file (WAV, FLAC, Ogg, or MP3). The audio is loaded directly and made available through the same ARA opcodes, making it straightforward to develop and debug without leaving your normal Cabbage workflow.

See the [ARA Opcodes](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGetSourceCount) reference for the full list of available opcodes.

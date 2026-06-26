---
title: ARA Support
description: Using ARA (Audio Random Access) with Cabbage 3
---

**Audio Random Access (ARA)** is an extension to the standard audio plugin format that gives a plugin direct, offline access to a host's audio material—without having to process it in real time. **Cabbage 3** supports ARA through a consolidated opcode API that provides access to the host's audio tracks. 
   
In an ARA document, you'll find references to several key entities:

* **Audio Sources (`AudioSource`):** Provide the low-level PCM data and properties for any audio asset loaded into a DAW session. >Note: AudioSource's have their own playbackRegions, don't confuse these with the higer level PlaybackRegions listed below. 
* **Playback Regions (`PlaybackRegion`):** Represent how an audio source is mapped onto the DAW timeline as a clip. It contains information about the region's duration, its start time on the DAW timeline, and its internal start time/offset relative to the raw audio file. Cropping the start or end of an audio clip in the DAW will modify this `PlaybackRegion` structure. Note that duplicating an audio source across multiple tracks will increase the number of regions, but not the number of audio sources. 
* **Region Sequences (`RegionSequence`):** Represent a collection of playback regions grouped together, typically mapping to tracks, lanes, or channels in the host.
* **View Selection (`ViewSelection`):** Provides real-time information about the host's current user selection, which can include specific playback regions, region sequences, and/or a distinct time range.


### Exporting an ARA plugin

ARA support is only available in dedicated ARA build targets. When exporting your plugin from the Cabbage extension, you must choose one of the ARA-specific export commands:

- **Export as VST3 Effect (ARA)**
- **Export as VST3 Synth (ARA)**

These commands are available from the VS Code Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux). Exporting with a standard VST3 or CLAP target will produce a plugin that does not include ARA support.

### How it works

When an ARA-capable host loads a Cabbage plugin, it grants the plugin direct access to the audio material on each track. Cabbage reads this audio data directly from the host, stores it in an internal data pool, and makes it available to your Csound instrument through the `cabbageAraGet` opcode.

All Cabbage ARA plugin instances in a project share one document model. That model can contain many audio sources (for example, across multiple tracks). Cabbage provides opcodes to query source metadata, read audio samples, and detect when the model is updated.

### Querying source metadata

Use `cabbageAraGet` to query information about the available audio sources. Top-level properties (like `currentIndex` and `audioSourceCount`) are queried without an index. Per-source metadata (like `audioSource.name`, `audioSource.channels`, and `audioSource.duration`) takes a source index argument.

```csound
instr 1
  iIdx   cabbageAraGet "currentIndex"
  iCnt   cabbageAraGet "audioSourceCount"
  SName  cabbageAraGet "audioSource.name", iIdx
  iCh    cabbageAraGet "audioSource.channels", iIdx
  iN     cabbageAraGet "audioSource.sampleCount", iIdx
  iSr    cabbageAraGet "audioSource.sampleRate", iIdx
  iDur   cabbageAraGet "audioSource.duration", iIdx

  prints("Source '%s': %d ch, %d samples, %d Hz, %.2f sec\n",
         SName, iCh, iN, iSr, iDur)
endin
```

:::note
Property names use dot notation to express the data hierarchy. For example, `audioSource.region.start` queries the crop start position of the audio source. Properties ending in `InSamples` are in samples at the source's sample rate; without the suffix, they're in seconds.
:::

### Reading audio data

Use `cabbageAraGetSourceSamples` to read raw PCM data from a source. It supports audio-rate, k-rate, and array output. To read the contents of the track the plugin is currently loaded onto, do this:

```csound
instr 1
  iIdx  cabbageAraGet "currentIndex"
  iN    cabbageAraGet "audioSource.sampleCount", iIdx
  ; Read samples from channel 0 as a k-rate array
  kSamples[] = cabbageAraGetSourceSamples(0, iN, 0, iIdx)

  ; Or read sample-by-sample at audio rate
  aPhase phasor sr / iN
  sig:a = cabbageAraGetSourceSamples(aPhase, 0, iIdx)
  out(sig, sig)
endin
```

### Detecting updates

`cabbageAraGetUpdate` returns a k-rate counter that increments whenever the ARA model data changes. Use it as a trigger to re-read source metadata. This fires whenever changes are made to the session — timeline edits, new clips added, clips resized, tracks hidden, etc.

```csound
instr 1
    updated:k = cabbageAraGetUpdate()
    if changed:k(updated) == 1 then
        event "i", "ReadAraData", 0, 3600
    endif
endin

instr ReadAraData
  iIdx cabbageAraGet "currentIndex"
  iCnt cabbageAraGet "audioSourceCount"
  SLast cabbageAraGet "lastEvent"
  prints("Update [%s]: source %d of %d\n", SLast, iIdx, iCnt)
endin
```

### AudioSource Playback regions

ARA hosts define audio source playback regions that specify which portion of a source is active. Use the region properties to query these:

```csound
instr 1
  iIdx    cabbageAraGet "currentIndex"
  iStart  cabbageAraGet "audioSource.region.startInSamples", iIdx
  iCount  cabbageAraGet "audioSource.region.durationInSamples", iIdx
  iDur    cabbageAraGet "audioSource.duration", iIdx

  prints("Region: sample %d, %d samples (%.2f sec)\n", iStart, iCount, iDur)
endin
```

### All playback regions in the session

List all clips in the document (not just the selected ones), using the `playbackRegionCount` property and per-index `playbackRegion.*` properties. This gives you access to every clip on the timeline, including its crop offset within the source and its arrangement position:

```csound
instr 1
  kTrig cabbageAraGetUpdate
  if kTrig == 1 then
    event "i", "ShowAllClips", 0, 1
  endif
endin

instr ShowAllClips
  iCnt cabbageAraGet "playbackRegionCount"
  prints("%d clips in session:\n", iCnt)
  idx = 0
  while idx < iCnt do
    SName cabbageAraGet "playbackRegion.name", idx
    STrack cabbageAraGet "playbackRegion.sequenceName", idx
    iStart cabbageAraGet "playbackRegion.startInSamples", idx
    iDur   cabbageAraGet "playbackRegion.durationInSamples", idx
    iPbStart cabbageAraGet "playbackRegion.start", idx
    iPbDur   cabbageAraGet "playbackRegion.duration", idx
    iSrcIdx  cabbageAraGet "playbackRegion.sourceIndex", idx
    prints("  [%d] '%s' on '%s': src#%d crop=%d-%d pb=%.3f-%.3f\n",
           idx, SName, STrack, iSrcIdx, iStart, iStart+iDur, iPbStart, iPbStart+iPbDur)
    idx += 1
  od
endin
```

The playback region array is automatically maintained via ARA lifecycle callbacks — clips are added when `playbackRegionAddedToRegionSequence` fires and removed when `playbackRegionRemovedFromRegionSequence` or `playbackRegionWillDestroy` fires. 
> The difference an audio source region, and a playbackRegion is that a single audio source will only have a single playback region. While a single audio source may have multiple playback regions if it is placed across several tracks. 

### EditorView selection

When the user selects tracks or regions in the host, the plugin is notified via the EditorView. Selection data is accessible through indexed properties — use `editorView.selectedPlaybackRegionCount` to get the number of selected playback regions (clips), then query each by index:

```csound
instr 1
  kTrig cabbageAraGetUpdate
  if kTrig == 1 then
    event "i", "ShowSelection", 0, 1
  endif
endin

instr ShowSelection
  iCnt    cabbageAraGet "editorView.selectedPlaybackRegionCount"
  iHidden cabbageAraGet "editorView.hiddenSequenceCount"
  prints("%d regions selected (%d tracks hidden):\n", iCnt, iHidden)
  idx = 0
  while idx < iCnt do
    SName  cabbageAraGet "editorView.selectedRegion.name", idx
    iStart cabbageAraGet "editorView.selectedRegion.startInSamples", idx
    iDurSec cabbageAraGet "editorView.selectedRegion.duration", idx
    iDurSamp cabbageAraGet "editorView.selectedRegion.durationInSamples", idx
    prints("  [%d] '%s' start=%d dur=%.3fs (%d samples)\n", idx, SName, iStart, iDurSec, iDurSamp)
    idx += 1
  od
endin
```

The `"lastEvent"` property will be `"notifySelection"` when the selection changes, or `"notifyHideRegionSequences"` when tracks are hidden or shown. Selection index is separate from source pool index — the first selected region is always index 0 regardless of which source it belongs to.

### Testing without a DAW (CabbageApp)

During development, you can test ARA instruments without an ARA-capable host by using CabbageApp's standalone mode. There are two ways to provide audio files for testing:

**VS Code extension prompt:** When the VS Code extension launches a standalone ARA instrument, it will prompt you to select an audio file (WAV, FLAC, Ogg, or MP3).

**Widget JSON property:** You can pre-specify test files in the widget JSON so they load automatically without a prompt:

```json
{
  "ara": {
    "testFiles": ["guitar.wav", "drums.wav"]
  }
}
```

Relative paths are resolved from the CSD file's directory. The audio is loaded on a background thread and made available through the same ARA opcodes, making it straightforward to develop and debug without leaving your normal Cabbage workflow.

### Current limitations

The ARA implementation is still in its early stages. The following ARA entities are not yet fully exposed through the opcode API:

| ARA Entity | Status | Notes |
|---|---|---|
| AudioSource | Supported | Name, channels, sample count, sample rate, duration, region crop |
| PlaybackRegion | Supported | Name, track name, crop offset, arrangement position, source index |
| EditorView selection | Supported | Selected region/track data, time range, hidden tracks |
| MusicalContext | Not exposed | Callbacks fire events but properties (name, order index) are not stored |
| RegionSequence | Partial | Track name captured via playback region, but standalone properties (order index) not exposed |
| AudioModification | Not exposed | Used internally but not accessible through opcodes |

This will be expanded in future versions as the ARA integration matures.

See the [ARA Opcodes](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGet) reference for the full list of available opcodes.

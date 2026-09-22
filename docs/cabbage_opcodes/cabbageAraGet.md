---
title: cabbageAraGet
description: Query ARA source metadata and state from a consolidated JSON store
---

# cabbageAraGet

Returns metadata about ARA audio sources, region information, and plugin state from a consolidated JSON data store. Available in numeric and string variants.

## Synopsis

```csound
iVal cabbageAraGet "property"
iVal cabbageAraGet "property", iIndex
SVal cabbageAraGet "property"
SVal cabbageAraGet "property", iIndex
```

## Description

`cabbageAraGet` is the primary opcode for querying ARA session data. It reads from a thread-safe JSON store that is updated automatically whenever the host's document model changes. All values are returned at i-rate (init pass only).

Property names use dot notation to express the data hierarchy. For example, `audioSource.region.start` queries the crop start position of the audio source. The index argument selects which item to query — the meaning depends on the property prefix (source index, selection index, or playback region index).

## Time Units

ARA properties use two time domains, and the naming convention reflects this:

- **Source-relative properties** (crop position within the audio file) are available in both **seconds** and **samples** at the source's sample rate. Properties ending in `InSamples` are in samples; without the suffix, they're in seconds. For example, `audioSource.region.start` is in seconds, while `audioSource.region.startInSamples` is in samples.

- **Arrangement properties** (where a clip sits on the host timeline) are given in **seconds**. These have no `InSamples` variant because the host's playback position is based on the host SR, which can change, whereas the time the clip appears will be the same regardless of the SR. For example, `playbackRegion.start` and `editorView.selectedPlayback.start`.

This follows the ARA API design: source file time is based in samples; arrangement time is not.

## Top-level Properties

These are queried without an index:

| Property | Type | Description |
|---|---|---|
| `"currentIndex"` | number | Index of the audio source associated with this plugin instance |
| `"update"` | number | Counter that increments on each ARA model change |
| `"lastEvent"` | string | Name of the most recent ARA lifecycle callback (see table below) |
| `"audioSourceCount"` | number | Total number of audio sources in the document. Sources will never be duplicated. |
| `"playbackRegionCount"` | number | Total number of playback regions (clips) in the document. A single source can account for multiple clips. |
| `"musicalContextCount"` | number | Total number of musical contexts in the document |
| `"regionSequenceCount"` | number | Total number of region sequences (tracks) in the document |
| `"audioModificationCount"` | number | Total number of audio modifications in the document |
| `"editorView.selectedPlaybackRegionCount"` | number | Number of playback regions (clips) in the current selection |

## Audio Source Properties

These query properties of the audio source file itself. Use the source pool index (the index of the audio source within the document):

| Property | Type | Index | Description |
|---|---|---|---|
| `"audioSource.name"` | string | source idx | File name or display name of the audio source |
| `"audioSource.channels"` | number | source idx | Number of audio channels (1 = mono, 2 = stereo) |
| `"audioSource.sampleCount"` | number | source idx | Total number of audio samples in the source file |
| `"audioSource.sampleRate"` | number | source idx | Sample rate in Hz (e.g. 44100, 48000) |
| `"audioSource.duration"` | number | source idx | Duration in seconds |

## Region Properties

These query the crop/edit state of a source within its audio modification. The values represent the position and duration of the audio source as cropped by the host. Use the source pool index:

| Property | Type | Index | Description |
|---|---|---|---|
| `"audioSource.region.start"` | number | source idx | Crop start position in seconds |
| `"audioSource.region.startInSamples"` | number | source idx | Crop start position in samples (within the source file) |
| `"audioSource.region.duration"` | number | source idx | Crop duration in seconds |
| `"audioSource.region.durationInSamples"` | number | source idx | Crop duration in samples |

📃 **Note:** `audioSource.region.start`/`audioSource.region.duration` and `audioSource.region.startInSamples`/`audioSource.region.durationInSamples` represent the same crop offset in different units.


## EditorView Properties

These query the current host selection and visibility state.

### Selection Overview

These are queried without an index:

| Property | Type | Description |
|---|---|---|
| `"editorView.timeRange.start"` | number | Start of the overall selection on the host arrangement timeline (seconds) |
| `"editorView.timeRange.duration"` | number | Duration of the overall selection on the host arrangement timeline (seconds) |
| `"editorView.hiddenSequenceCount"` | number | Number of hidden region sequences (tracks) |

### Selection Region Properties

These query individual selected playback regions (clips on the timeline). Use a selection index (not the source pool index):

| Property | Type | Index | Description |
|---|---|---|---|
| `"editorView.selectedRegion.name"` | string | selection idx | Name of the selected playback region at index |
| `"editorView.selectedRegion.startInSamples"` | number | selection idx | Start position in samples (modification time) |
| `"editorView.selectedRegion.duration"` | number | selection idx | Duration in seconds |
| `"editorView.selectedRegion.durationInSamples"` | number | selection idx | Duration in samples |
| `"editorView.selectedPlayback.start"` | number | selection idx | Where the selected playback region sits on the host arrangement timeline (seconds) |
| `"editorView.selectedPlayback.duration"` | number | selection idx | Duration of the selected playback region on the host arrangement timeline (seconds) |

📃 **Note:** Selection properties are indexed by position within the selection, not by source pool index. These are separate index spaces.


## Musical Context Properties

A musical context describes the rhythmic and harmonic structure of the music. Each document can contain multiple musical contexts. Use the musical context index:

| Property | Type | Index | Description |
|---|---|---|---|
| `"musicalContextCount"` | number | none | Total number of musical contexts in the document |
| `"musicalContext.name"` | string | mc idx | Display name of the musical context (may be empty) |
| `"musicalContext.orderIndex"` | number | mc idx | Sort order index within the document |
| `"musicalContext.color.r"` | number | mc idx | Red channel (0.0–1.0) |
| `"musicalContext.color.g"` | number | mc idx | Green channel (0.0–1.0) |
| `"musicalContext.color.b"` | number | mc idx | Blue channel (0.0–1.0) |

📃 **Note:** Colour values are returned as `0.0` if the host does not provide a colour for the musical context.


## Region Sequence Properties

A region sequence represents a track or lane in the host, containing playback regions. Each region sequence belongs to a musical context. Use the region sequence index:

| Property | Type | Index | Description |
|---|---|---|---|
| `"regionSequenceCount"` | number | none | Total number of region sequences (tracks) in the document |
| `"regionSequence.name"` | string | rs idx | Display name of the region sequence (may be empty) |
| `"regionSequence.orderIndex"` | number | rs idx | Sort order index within its musical context |
| `"regionSequence.musicalContextIndex"` | number | rs idx | Index of the parent musical context |
| `"regionSequence.color.r"` | number | rs idx | Red channel (0.0–1.0) |
| `"regionSequence.color.g"` | number | rs idx | Green channel (0.0–1.0) |
| `"regionSequence.color.b"` | number | rs idx | Blue channel (0.0–1.0) |

📃 **Note:** Region sequence index is separate from playback region index and source pool index. The track name is also available via `playbackRegion.sequenceName` for convenience.


## Audio Modification Properties

An audio modification represents a set of edits applied to an audio source. Each modification belongs to an audio source and can contain multiple playback regions. Use the modification index:

| Property | Type | Index | Description |
|---|---|---|---|
| `"audioModificationCount"` | number | none | Total number of audio modifications in the document |
| `"audioModification.name"` | string | mod idx | Display name of the modification (may be empty) |
| `"audioModification.persistentId"` | string | mod idx | Persistent ID used for archiving/restoring state |


## Playback Regions

These query all playback regions (clips) in the document, not just the selected ones. Use the playback region index (0-based, in the order they were added to the document):

| Property | Type | Index | Description |
|---|---|---|---|
| `"playbackRegion.name"` | string | pr idx | Source file name for this playback region |
| `"playbackRegion.sequenceName"` | string | pr idx | Track/lane name this playback region belongs to |
| `"playbackRegion.startInSamples"` | number | pr idx | Crop start position in samples (within the source) |
| `"playbackRegion.durationInSamples"` | number | pr idx | Crop duration in samples |
| `"playbackRegion.start"` | number | pr idx | Arrangement position on the host timeline (seconds) |
| `"playbackRegion.duration"` | number | pr idx | Duration on the host arrangement timeline (seconds) |
| `"playbackRegion.sourceIndex"` | number | pr idx | Source pool index for this playback region's source |
| `"playbackRegion.color.r"` | number | pr idx | Red channel (0.0–1.0) |
| `"playbackRegion.color.g"` | number | pr idx | Green channel (0.0–1.0) |
| `"playbackRegion.color.b"` | number | pr idx | Blue channel (0.0–1.0) |

📃 **Note:**
Playback region index is separate from source pool index and selection index. The playback region array is updated via ARA lifecycle callbacks (`playbackRegionAddedToRegionSequence`, `playbackRegionRemovedFromRegionSequence`, `playbackRegionPropertiesUpdated`, `playbackRegionWillDestroy`).


## Examples

### Basic source info

```csound
instr 1
  iIdx   cabbageAraGet "currentIndex"
  iCnt   cabbageAraGet "audioSourceCount"
  SName  cabbageAraGet "audioSource.name", iIdx
  iCh    cabbageAraGet "audioSource.channels", iIdx
  iSr    cabbageAraGet "audioSource.sampleRate", iIdx
  iDur   cabbageAraGet "audioSource.duration", iIdx

  prints("Source '%s': %d ch, %d Hz, %.2f sec\n", SName, iCh, iSr, iDur)
endin
```

### Reading crop region state

```csound
instr 1
  iIdx cabbageAraGet "currentIndex"
  iStartSamp cabbageAraGet "audioSource.region.startInSamples", iIdx
  iDurSamp   cabbageAraGet "audioSource.region.durationInSamples", iIdx
  iStartSec  cabbageAraGet "audioSource.region.start", iIdx
  iDurSec    cabbageAraGet "audioSource.region.duration", iIdx

  prints("Crop: sample %d-%d (%.3f-%.3f sec)\n", iStartSamp, iStartSamp+iDurSamp, iStartSec, iStartSec+iDurSec)
endin
```

### Reading the current selection

```csound
instr 1
  kTrig cabbageAraGetUpdate
  if kTrig == 1 then
    event "i", "ShowSelection", 0, 1
  endif
endin

instr ShowSelection
  iCnt   cabbageAraGet "editorView.selectedPlaybackRegionCount"
  iHidden cabbageAraGet "editorView.hiddenSequenceCount"
  prints("%d regions selected (%d tracks hidden):\n", iCnt, iHidden)
  idx = 0
  while idx < iCnt do
    SName cabbageAraGet "editorView.selectedRegion.name", idx
    iStart cabbageAraGet "editorView.selectedRegion.startInSamples", idx
    iDurSec cabbageAraGet "editorView.selectedRegion.duration", idx
    iDurSamp cabbageAraGet "editorView.selectedRegion.durationInSamples", idx
    prints("  [%d] '%s' start=%d dur=%.3fs (%d samples)\n", idx, SName, iStart, iDurSec, iDurSamp)
    idx += 1
  od
endin
```

### Reading audio samples (separate opcode)

```csound
instr 1
  iIdx cabbageAraGet "currentIndex"
  iN   cabbageAraGet "audioSource.sampleCount", iIdx

  ; Read all samples from channel 0 as a k-rate array
  kSamples[] cabbageAraGetSourceSamples 0, iN, 0, iIdx

  ; Or read sample-by-sample at audio rate
  aPhase phasor sr / iN
  aOut cabbageAraGetSourceSamples aPhase, 0, iIdx
endin
```

### Iterating all playback regions in the session

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
    iColR   cabbageAraGet "playbackRegion.color.r", idx
    iColG   cabbageAraGet "playbackRegion.color.g", idx
    iColB   cabbageAraGet "playbackRegion.color.b", idx
    prints("  [%d] '%s' on '%s': src#%d pb=%.3f-%.3f\n",
           idx, SName, STrack, iSrcIdx, iPbStart, iPbStart+iPbDur)
    prints("        colour: (%.2f, %.2f, %.2f)\n", iColR, iColG, iColB)
    idx += 1
  od
endin
```

### Iterating musical contexts

```csound
instr ShowMusicalContexts
  iCnt cabbageAraGet "musicalContextCount"
  prints("%d musical contexts:\n", iCnt)
  idx = 0
  while idx < iCnt do
    SName cabbageAraGet "musicalContext.name", idx
    iOrder cabbageAraGet "musicalContext.orderIndex", idx
    iColR cabbageAraGet "musicalContext.color.r", idx
    iColG cabbageAraGet "musicalContext.color.g", idx
    iColB cabbageAraGet "musicalContext.color.b", idx
    prints("  [%d] '%s' order=%d colour=(%.2f, %.2f, %.2f)\n",
           idx, SName, iOrder, iColR, iColG, iColB)
    idx += 1
  od
endin
```

### Iterating region sequences (tracks)

```csound
instr ShowRegionSequences
  iCnt cabbageAraGet "regionSequenceCount"
  prints("%d region sequences:\n", iCnt)
  idx = 0
  while idx < iCnt do
    SName cabbageAraGet "regionSequence.name", idx
    iOrder cabbageAraGet "regionSequence.orderIndex", idx
    iMcIdx cabbageAraGet "regionSequence.musicalContextIndex", idx
    iColR cabbageAraGet "regionSequence.color.r", idx
    iColG cabbageAraGet "regionSequence.color.g", idx
    iColB cabbageAraGet "regionSequence.color.b", idx
    prints("  [%d] '%s' order=%d context=#%d colour=(%.2f, %.2f, %.2f)\n",
           idx, SName, iOrder, iMcIdx, iColR, iColG, iColB)
    idx += 1
  od
endin
```

### Iterating audio modifications

```csound
instr ShowAudioModifications
  iCnt cabbageAraGet "audioModificationCount"
  prints("%d audio modifications:\n", iCnt)
  idx = 0
  while idx < iCnt do
    SName cabbageAraGet "audioModification.name", idx
    SId   cabbageAraGet "audioModification.persistentId", idx
    prints("  [%d] '%s' id='%s'\n", idx, SName, SId)
    idx += 1
  od
endin
```

## Notes

- All values are i-rate: call during `init` or inside an i-rate instrument triggered by `cabbageAraGetUpdate`.
- The JSON store is updated on a background thread when the host modifies the document. Use `cabbageAraGetUpdate` as a trigger to know when to re-read values.
- String values are allocated once at init and remain valid for the instrument's lifetime.

## See Also

- [cabbageAraGetUpdate](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGetUpdate)
- [cabbageAraGetSourceSamples](/cabbage3docs/docs/cabbage_opcodes/cabbageAraGetSourceSamples)

---

## Appendix: ARA Callback Event Types

The `"lastEvent"` top-level property returns one of the following strings, indicating which ARA callback was most recently fired:

### Editing Cycle

| Event | Description |
|---|---|
| `"beginEditing"` | Host started an edit gesture |
| `"endEditing"` | Host ended an edit gesture |

### Document Graph Changes

| Event | Description |
|---|---|
| `"musicalContextAddedToDocument"` | New musical context added |
| `"musicalContextRemovedFromDocument"` | Musical context removed |
| `"regionSequenceAddedToDocument"` | New region sequence (track) added |
| `"regionSequenceRemovedFromDocument"` | Region sequence removed |
| `"audioSourceAddedToDocument"` | New audio source added |
| `"audioSourceRemovedFromDocument"` | Audio source removed |
| `"documentWillDestroy"` | Document is about to be destroyed |

### Document Property Updates

| Event | Description |
|---|---|
| `"documentPropertiesUpdated"` | Document properties changed (did) |
| `"documentPropertiesWillUpdate"` | Document properties about to change (will) |
| `"musicalContextPropertiesUpdated"` | Musical context properties changed |
| `"musicalContextPropertiesWillUpdate"` | Musical context properties about to change |
| `"regionSequencePropertiesUpdated"` | Region sequence properties changed |
| `"regionSequencePropertiesWillUpdate"` | Region sequence properties about to change |
| `"audioSourcePropertiesUpdated"` | Audio source properties changed |
| `"audioSourcePropertiesWillUpdate"` | Audio source properties about to change |
| `"audioModificationPropertiesUpdated"` | Audio modification properties changed |
| `"audioModificationPropertiesWillUpdate"` | Audio modification properties about to change |
| `"playbackRegionPropertiesWillUpdate"` | Playback region properties about to change |

### Region Sequence Lifecycle

| Event | Description |
|---|---|
| `"regionSequenceAddedToMusicalContext"` | Region sequence added to a musical context |
| `"regionSequenceRemovedFromMusicalContext"` | Region sequence removed from a musical context |
| `"musicalContextWillDestroy"` | Musical context about to be destroyed |
| `"regionSequenceWillDestroy"` | Region sequence about to be destroyed |

### Audio Source/Modification Lifecycle

| Event | Description |
|---|---|
| `"audioSourceWillDestroy"` | Audio source about to be destroyed |
| `"audioModificationAddedToAudioSource"` | New modification added to a source |
| `"audioModificationRemovedFromAudioSource"` | Modification removed from a source |
| `"audioModificationWillDestroy"` | Audio modification about to be destroyed |
| `"audioSourceDeactivatedForUndo"` | Source deactivated for undo history |
| `"audioSourceReactivatedFromUndo"` | Source reactivated after undo |
| `"audioModificationDeactivatedForUndo"` | Modification deactivated for undo |
| `"audioModificationReactivatedFromUndo"` | Modification reactivated after undo |

### Playback Region Lifecycle

| Event | Description |
|---|---|
| `"playbackRegionAddedToRegionSequence"` | Playback region added to a region sequence |
| `"playbackRegionRemovedFromRegionSequence"` | Playback region removed from a region sequence |
| `"playbackRegionAddedToAudioModification"` | Playback region added to a modification |
| `"playbackRegionRemovedFromAudioModification"` | Playback region removed from a modification |
| `"playbackRegionWillDestroy"` | Playback region about to be destroyed |

### EditorView

| Event | Description |
|---|---|
| `"notifySelection"` | Host sent a new selection (user selected regions/tracks) |
| `"notifyHideRegionSequences"` | Host updated hidden/shown tracks |

---
title: ARA Support
description: Using ARA (Audio Random Access) with Cabbage 3
---

ARA (Audio Random Access) is an extension to the standard audio plugin format that gives a plugin direct, offline access to a host's audio material — without having to process it in real time. Cabbage supports ARA through a companion `.ara.csd` file that runs an offline Csound analysis pass and feeds the results back into the main instrument.

### Exporting an ARA plugin

ARA support is only available in dedicated ARA build targets (see below for details on developing ARA instrument outside a DAW). When exporting your plugin from the Cabbage extension, you must choose one of the ARA-specific export commands:

- **Export as VST3 Effect (ARA)**
- **Export as VST3 Synth (ARA)**

These commands are available from the VS Code Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux). Exporting with a standard VST3 or CLAP target will produce a plugin that does not include ARA support, even if a companion `.ara.csd` file is present.

### How it works

When Cabbage loads a plugin, it looks for a companion file alongside your main `.csd`:

```csound
MyInstrument.csd          ← main instrument
MyInstrument.ara.csd      ← ARA analysis script (optional)
```

If the companion file is found, Cabbage reads the `<CabbageARA>` section to discover which Csound channels the analysis script will write. After the host grants sample access, Cabbage runs the `.ara.csd` offline — feeding the audio data in block by block — and then writes the resulting channel values back into the main Csound instance.

In ARA, all plugin instances in a project share one ARA document model. That model can contain many audio sources (for example, across multiple tracks). To support this, Cabbage forwards analysis results as arrays in the main instrument: each source occupies one array index.

### The `<CabbageARA>` section

Add a `<CabbageARA>` block to your `.ara.csd` file to declare the output channels your analysis script produces. The `<CabbageARA>` object supports:

- `channels` (required): array of channel definitions produced by the analysis pass
- `testFile` (optional): local audio file path used by VS Code extension for standalone ARA testing.

Each item in `channels` has two fields:

| Field  | Values            | Description                                      |
|--------|-------------------|--------------------------------------------------|
| `id`   | any string        | The Csound channel name written by the analysis  |
| `type` | `number`, `string`| The channel type; string values may contain JSON |

Example including `testFile`:

```csound
<CabbageARA>
{
  "channels": [
    { "id": "ara_tempo", "type": "number" }
  ],
  "testFile": "/path/to/your/audio.wav"
}
</CabbageARA>
```

### Writing analysis results

Inside the `<CsInstruments>` instrument section of your `.ara.csd`, write values to the declared channels during performance:

```csound
<CabbageARA>
{
  "channels": [
    { "id": "lufs", "type": "number" }
  ],
  "testFile": "/path/to/your/audio.wav"
}
</CabbageARA>
<CsInstruments>
sr     = 44100
ksmps  = 512
nchnls = 2
0dbfs  = 1

instr 1
  ; These channels are set automatically by Cabbage before performance:
  ; ARA_SOURCE_NAME      — source file name (string)
  ; ARA_SOURCE_SAMPLES   — total sample count
  ; ARA_SOURCE_SR        — sample rate
  ; ARA_SOURCE_CHANNELS  — channel count
  ; ARA_SOURCE_DURATION  — duration in seconds

  in1:a, in2:a  = ins()
  mom:k, int:k, short:k = lufs(0, in1, in2)
  ; ARA_ENDED is set to 1 on the final k-cycle — write final k-rate results here.
  kEnded = chnget:k("ARA_ENDED")
  if kEnded == 1 then
    //set final data here
  endif
endin
</CsInstruments>
```

📃 **Note:** The `ARA_ENDED` channel will be set to 1 after all samples have been processed. While you can write data continuously to named channels during processing, it is often more efficient to compute the data and write it once at the end of the performance.

After the analysis pass completes, any declared channels are forwarded to the main Csound. They can be queried using `chnget` and `chnset`.

In the main instrument, each declared channel is exposed as a array channel. Although 64 slots are allocated internally, the number of valid entries is given by `ARA_SOURCE_COUNT`.

Source metadata is also exposed as arrays using plural names:

- `ARA_SOURCE_NAMES`:  all source file names (string)
- `ARA_SOURCE_SAMPLES`: total sample count across all sources
- `ARA_SOURCE_SRS`: sample rates for all sources
- `ARA_SOURCE_CHANNELS`: channel counts for all sources
- `ARA_SOURCE_DURATIONS`: duration in seconds for all sources

### Reading results in the main instrument

Once analysis is complete, read declared channels as arrays, then index with `ARA_CURRENT_SOURCE_INDEX`. 

```csound
count:i = chnget("ARA_SOURCE_COUNT")
index:i = chnget("ARA_CURRENT_SOURCE_INDEX")
sources:S[] = chnget:S[]("ARA_SOURCE_NAMES")
LUFS:i[]   chnget "lufs"

prints("LUFS Value for %s is %d", sources[index], LUFS[index])
```

`ARA_CURRENT_SOURCE_INDEX` points to the source associated with the current plugin instance/track. This is subject to change depending on DAW events that are taking place across a session, but it will always give the index of the source associated with the track a plugin is attached to. See note below about how best to handle this changing data. 

`ARA_SOURCE_COUNT` tells you how many source entries are valid.

`ARA_UPDATE` is incremented at k-rate whenever the ARA model data is refreshed.

For robust instrument design, use `ARA_UPDATE` as a trigger to launch an instrument that reads the array data at i-time. This avoids timing ambiguity and keeps update handling deterministic. 

Example trigger pattern:

```csound
instr 1
  update:k = chnget:k("ARA_UPDATE")
  trig:k = changed:k("update")
  if trig == 1 then
    event( "i", "ReadAraData", 0, 0.001 )
  endif
endin

instr ReadAraData
  count:i = chnget("ARA_SOURCE_COUNT")
  index:i = chnget("ARA_CURRENT_SOURCE_INDEX")
  sources:S[] = chnget:S[]("ARA_SOURCE_NAMES")
  LUFS:i[]   chnget "lufs"
endin
```

### Reserved channels

Cabbage automatically sets the following read-only channels in the `.ara.csd` before the performance loop starts:

| Channel               | Type   | Description                                         |
|-----------------------|--------|-----------------------------------------------------|
| `ARA_SOURCE_NAME`     | string | Name of the audio source                            |
| `ARA_SOURCE_SAMPLES`  | number | Total number of samples                             |
| `ARA_SOURCE_SR`       | number | Sample rate                                         |
| `ARA_SOURCE_CHANNELS` | number | Number of audio channels                            |
| `ARA_SOURCE_DURATION` | number | Duration in seconds                                 |
| `ARA_ENDED`           | number | Set to `1` on the final k-cycle of the analysis pass — use this to trigger any end-of-analysis writes |

In the main instrument, Cabbage also provides:

| Channel                    | Type   | Description |
|----------------------------|--------|-------------|
| `ARA_SOURCE_NAMES`         | string | Per-source array of source names |
| `ARA_SOURCE_SAMPLES`       | number | Per-source array of sample counts |
| `ARA_SOURCE_SRS`           | number | Per-source array of sample rates |
| `ARA_SOURCE_CHANNELS`      | number | Per-source array of channel counts |
| `ARA_SOURCE_DURATIONS`     | number | Per-source array of durations in seconds |
| `ARA_SOURCE_COUNT`         | number | Number of valid source entries currently present in the shared ARA model |
| `ARA_CURRENT_SOURCE_INDEX` | number | Index of the source associated with this plugin instance/track |
| `ARA_CURRENT_SOURCE_NAME`  | string | Convenience scalar name for the currently indexed source |
| `ARA_UPDATE`               | number | Monotonic update counter incremented when forwarded ARA data changes |

### Testing without a DAW (CabbageApp)

During development, you can use the optional `testFile` attribute in `<CabbageARA>` (shown above) to test ARA analysis without an ARA-capable host.

When CabbageApp detects a `.ara.csd` companion file with a `testFile` path it will automatically read the audio file (WAV, FLAC, Ogg, and MP3 are supported) and run the analysis pass, making it straightforward to develop and debug analysis scripts without leaving your normal Cabbage workflow.

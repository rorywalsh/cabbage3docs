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

```
MyInstrument.csd          ← main instrument
MyInstrument.ara.csd      ← ARA analysis script (optional)
```

If the companion file is found, Cabbage reads the `<CabbageARA>` section to discover which Csound channels the analysis script will write. After the host grants sample access, Cabbage runs the `.ara.csd` offline — feeding the audio data in block by block — and then writes the resulting channel values back into the main Csound instance.

### The `<CabbageARA>` section

Add a `<CabbageARA>` block to your `.ara.csd` file to declare the output channels your analysis script produces:

```json
<CabbageARA>
{
  "channels": [
    { "id": "ara_tempo",  "type": "number" },
    { "id": "ara_rms",    "type": "number" },
    { "id": "ara_source", "type": "string" }
  ]
}
</CabbageARA>
```

Each entry has two fields:

| Field  | Values            | Description                                      |
|--------|-------------------|--------------------------------------------------|
| `id`   | any string        | The Csound channel name written by the analysis  |
| `type` | `number`, `string`| The channel type; string values may contain JSON |

### Writing analysis results

Inside the `<Cabbage>` instrument section of your `.ara.csd`, write values to the declared channels at the end of performance:

```csound
<CsInstruments>
sr     = 44100
ksmps  = 512
nchnls = 2
0dbfs  = 1

instr 1
  ; ARA_SOURCE_* channels are set automatically by Cabbage before performance:
  ;   ARA_SOURCE_NAME      — source file name (string)
  ;   ARA_SOURCE_SAMPLES   — total sample count
  ;   ARA_SOURCE_SR        — sample rate
  ;   ARA_SOURCE_CHANNELS  — channel count
  ;   ARA_SOURCE_DURATION  — duration in seconds

  in1:a, in2:a  = ins()

  ; ARA_ENDED is set to 1 on the final k-cycle — write final results here.
  kEnded = chnget:k("ARA_ENDED")
  if kEnded == 1 then
    //set final data here
  endif
endin
</CsInstruments>
```

After the analysis pass completes, any declared channels are forwarded to the main Csound. They can be queired using the `chnget` and `chnset` opcodes. Note that in Csound 7, arrays can also be passed over named channels. 

### Reading results in the main instrument

Once analysis is complete the values are available as normal Csound channels:

```csound
rms:k = chnget:k("ara_rms")
tempo:k = chnget:k("ara_tempo")
sourcefile:S = chnget("ara_source")
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

### Testing without a DAW (CabbageApp)

During development you can test ARA analysis without an ARA-capable host by adding a `"testFile"` field to your `<CabbageARA>` section:

```json
<CabbageARA>
{
  "channels": [
    { "id": "ara_tempo", "type": "number" }
  ],
  "testFile": "/path/to/your/audio.wav"
}
</CabbageARA>
```

When CabbageApp detects a `.ara.csd` companion file with a `testFile` path it will automatically read the audio file (WAV, FLAC, Ogg, and MP3 are supported) and run the analysis pass, making it straightforward to develop and debug analysis scripts without leaving your normal Cabbage workflow.

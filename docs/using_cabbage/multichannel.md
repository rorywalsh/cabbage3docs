---
title: Working with Multichannel Instruments
description: Managing multichannel setups
---

While any instrument that processes more than one signal channel can be considered multichannel, the term is typically used for instruments that handle more than two channels.

## Defining channel configuration

In Cabbage 3, the number of input and output channels is controlled exclusively by the `channelConfig` property within the JSON header. If no `channelConfig` is defined, the plugin defaults to a standard stereo configuration (2 in, 2 out). 

Cabbage dynamically overrides Csound’s internal channel settings to match the layout requested by the channelConfig or the host DAW. This ensures that Csound’s channel count always aligns perfectly with the DAW’s signal path or the hardware output when running in standalone mode. You can still query `nchnls` or `nchnls_i` within your orchestra code, but note they will given a value directly from the host.  

`channelConfig` is an array of named configurations. Each entry describes one layout that the host can choose from:

```json
"channelConfig": [
    { "name": "Stereo",    "ins": "2",   "outs": "2" },
    { "name": "Mono",      "ins": "1",   "outs": "1" }
]
```

The first entry is used on initial load. The host can switch between configurations at runtime (if it supports the CLAP audio ports config extension), and Cabbage will restart Csound with the correct channel count automatically.

📃 **Note:** `nchnls` and `nchnls_i` in the Csound `<CsInstruments>` block are ignored for routing purposes. Cabbage always sets Csound's channel count from `channelConfig`. You should still write `nchnls`/`nchnls_i` in your CSD if your Csound code depends on them internally, but they have no effect on what the host sees.

## Instruments with sidechains

A sidechain is an auxiliary input bus that a plugin uses as a control signal rather than as audio to process directly. A typical sidechain effect has a stereo main input and a separate mono sidechain input. In Cabbage, multiple input buses are expressed using `+` to separate the channel count of each bus:

```json
"channelConfig": [
    { "name": "Sidechain", "ins": "2+1", "outs": "2" },
    { "name": "Stereo",    "ins": "2",   "outs": "2" }
]
```

Here `"ins": "2+1"` means two buses on the input side: a stereo bus (2 channels) followed by a mono sidechain bus (1 channel). The same `+` notation works for outputs if you need multiple output buses.

In your Csound code the sidechain channels arrive after the main input channels, so for `"2+1"` inputs:

```csound
aL, aR     ins          ; main stereo input (channels 1 & 2)
aSide      inch 3       ; sidechain input   (channel 3)
```

## Multiple configurations

You can offer several configurations and let the host (or user) choose:

```json
"channelConfig": [
    { "name": "Stereo",          "ins": "2",   "outs": "2" },
    { "name": "Mono",            "ins": "1",   "outs": "1" },
    { "name": "Sidechain",       "ins": "2+1", "outs": "2" },
    { "name": "Quad",            "ins": "4",   "outs": "4" }
]
```

When a host changes the active configuration, Cabbage detects the channel count change and reinitialises Csound with the new values. It is good practice to write defensive Csound code that handles different channel counts at runtime (failure to do so will result in undefined behaviour):

```csound
if (nchnls == 1) then
    outs (aLeft + aRight) / 2
else
    outs aLeft, aRight
endif
```

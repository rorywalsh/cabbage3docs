---
title: Audio Channel Configuration
description: Managing channel layouts
---

Managing channel layouts presents a unique challenge because a developer cannot assume a host will honor the plugin's preferred configuration. For instance, a plugin designed for Stereo (2-in/2-out) might be forced onto a Mono or even a 5.1 track by the host. If the plugin attempts to access a channel index that the host hasn't allocated, it can result in a memory access violation or undefined behavior. Therefore, developers must implement defensive I/O logic (see below), verifying the actual channel count at runtime and gracefully handling any configuration the host provides. 


## Defining channel configuration

In Cabbage 3, the number of input and output channels is controlled exclusively by the `channelConfig` property within the JSON header. If no `channelConfig` is defined, the plugin defaults to a standard stereo configuration (2 in, 2 out). 

Cabbage dynamically overrides Csound’s internal channel settings to match the layout requested by the `channelConfig` or, more importantly, the host DAW. This ensures that Csound’s channel count always aligns perfectly with the DAW’s signal path or the hardware device when running in standalone mode. You can still query `nchnls` or `nchnls_i` within your orchestra code. They will always return the number of channels set by the host. 

`channelConfig` is an array of named configurations. Each entry describes one layout that the host can choose from:

```json
"channelConfig": [
    { "name": "Stereo",    "ins": "2",   "outs": "2" },
    { "name": "Mono",      "ins": "1",   "outs": "1" }
]
```

The first entry is used on initial load. The host can switch between configurations at runtime. Cabbage will restart Csound with the correct channel count automatically if the users changes the channel config. This could result in internal buffers being destroyed, but there is no way to avoud this 

📃 **Note:** While `channelConfig` object can be used to indicate the preferred channel configuration for a plugin, the host has the final say. So it's important to check `nhchnls` and `nchnls_i` within your code to make sure your instrument can correctly handle the channel layout. 

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

When a host changes the active configuration, Cabbage detects the channel count change and reinitialises Csound with the new values. The host does not always follow the channel layouts provided by the plugin. Therefore it is good practice to write defensive Csound code that handles different channel counts at runtime (failure to do so can result in undefined behaviour):

```csound
if (nchnls == 1) then
    out((aLeft + aRight) / 2)
else
    outs(aLeft, aRight)
endif
```

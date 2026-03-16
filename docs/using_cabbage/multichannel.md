---
title: Working with Multichannel Instruments
description: Managing multichannel setups
---

While any instrument that processes more than one signal channel can be considered multichannel, the term is typically used for instruments that handle more than two channels.

In a vanilla Csound instrument you would use `nchnls` and `nchnls_i` to declare the number of output and input channels respectively. In Cabbage, however, you should use the `channelConfig` object in the Cabbage JSON instead. The reason is that a plugin does not get to decide its own channel layout, that is ultimately up to the host DAW. All Cabbage can do is request a configuration and hope the host honours it. By declaring your layout through `channelConfig`, Cabbage can set `nchnls` and `nchnls_i` for you automatically and ensure the values stay consistent with what the host has actually granted.

📃 **Note:** If no `channelConfig` is provided, Cabbage falls back to whatever `nchnls` / `nchnls_i` values are present in the Csound header.

## Buses

An audio bus is a logical grouping of audio channels that allows for the routing and processing of multiple audio signals as a single unit. Buses enable plugins to handle mono, stereo, surround, or custom configurations and integrate cleanly with a DAW's mixing and routing workflows. Sidechaining, for example, is typically handled via a dedicated bus.

Define bus configurations at the **top level** of the Cabbage JSON using the `channelConfig` property. It accepts an object with `inputs` and `outputs` arrays. Each element in the array is a string that uses dot notation to list the channel count of each bus — for example `"2.1"` means a stereo bus followed by a mono bus.

### Stereo in, stereo out (simple effect)

```json
<Cabbage>{
    "pluginId": "def1",
    "channelConfig": {
        "inputs": ["2"],
        "outputs": ["2"]
    },
    "widgets": [
        {
            "type": "form",
            "caption": "Effect",
            "size": { "height": 300, "width": 580 }
        }
    ]
}</Cabbage>
```

- `"inputs": ["2"]` — one stereo input bus
- `"outputs": ["2"]` — one stereo output bus

### Two stereo input buses (dual-bus input)

Some workflows require two independent stereo inputs — for example, mixing two sources before processing. Use dot notation within the string to define multiple buses: `"2.2"` means two stereo buses.

```json
<Cabbage>{
    "pluginId": "def1",
    "channelConfig": {
        "inputs": ["2.2"],
        "outputs": ["2"]
    },
    "widgets": [
        {
            "type": "form",
            "caption": "Dual Input Effect",
            "size": { "height": 300, "width": 580 }
        }
    ]
}</Cabbage>
```

- `"inputs": ["2.2"]` — two stereo input buses (4 total input channels)
- `"outputs": ["2"]` — one stereo output bus

### Stereo + mono sidechain input

For the sidechain example above, group the main stereo input into one bus and the sidechain into a separate mono bus. Use `"2.1"` — two buses: stereo + mono.

```json
<Cabbage>{
    "pluginId": "def1",
    "channelConfig": {
        "inputs": ["2.1"],
        "outputs": ["2"]
    },
    "widgets": [
        {
            "type": "form",
            "caption": "Sidechain Effect",
            "size": { "height": 300, "width": 580 }
        }
    ]
}</Cabbage>
```

- `"inputs": ["2.1"]` — stereo main bus + mono sidechain bus (3 total input channels)
- `"outputs": ["2"]` — one stereo output bus

Some hosts may still override the requested bus configuration. For example, dropping an instrument onto a mono track in Logic will cause Logic to change the configuration to mono. In this case Cabbage will overwrite `nchnls` and set it to 1. It is therefore recommended to guard your output code:

```csound
if (nchnls == 1) then
    outs (aLeft+aRight)/2
else
    outs aLeft, aRight
endif
```

This prevents Csound from attempting to access a channel that the host has not made available.
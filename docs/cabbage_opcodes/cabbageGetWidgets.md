# cabbageGetWidgets

Returns a string array containing the IDs of all widgets currently loaded in the instrument. This opcode works at i-time only. Each entry in the returned array corresponds to a widget's top-level `id` field, or falls back to `channels[0].id` if no top-level `id` is present. This opcodes runs at i-time only. 

## Syntax
```csound
SWidgetIds[] = cabbageGetWidgets()
```

## Initialization

- `SWidgetIds[]` – a string array of widget IDs, one entry per widget in the current Cabbage layout.

## Example

```csound
<Cabbage>[
    {"type":"form","caption":"Simple Instrument","size":{"width":600,"height":300},"pluginId":"GWdt"},
    {"type":"rotarySlider","channel":"gain","bounds":{"left":50,"top":50,"width":100,"height":100},"range":{"min":0,"max":1,"value":0.5},"text":"Gain"},
    {"type":"button","channel":"trigger","bounds":{"left":200,"top":80,"width":80,"height":40},"text":{"on":"On","off":"Off"}}
]
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-dm0 -n
</CsOptions>
<CsInstruments>
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    ; Retrieve all widget IDs
    SWidgets[] = cabbageGetWidgets()
    i = 0
    while i < lenarray(SWidgets) do
        prints("Widget ID: %s\n", SWidgets[i])
        i += 1
    od
endin

</CsInstruments>
<CsScore>
i1 0 1
</CsScore>
</CsoundSynthesizer>
```

## Notes

- This opcode is i-time only; call it from an instrument that runs at initialisation, or from a always-on instrument (`i1 0 z`).
- The form widget is included in the returned array.
- If a widget has no `id` field and no `channels[0].id`, an empty string is returned for that entry.
- Combine with `cabbageGet` or `cabbageHasKey` to dynamically inspect widget properties at startup.

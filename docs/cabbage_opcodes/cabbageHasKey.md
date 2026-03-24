# cabbageHasKey

This opcode checks whether a named widget has a given property key. It supports dot-notation for nested JSON properties (e.g., `"bounds.left"`). Returns 1 if the key exists, 0 otherwise. It can run at init-time or k-time.

## Syntax
```csound
hasKey:i = cabbageHasKey(SChannel, SProperty)
hasKey:k = cabbageHasKey(SChannel, SProperty)
```

### Initialization
* *SChannel* – the name of the widget channel to query
* *SProperty* – the property key to check. Supports dot-notation for nested properties, e.g., `"bounds.left"`
* *hasKey* – 1 if the property exists on the widget, 0 otherwise

### Performance
* *hasKey* – 1 if the property exists on the widget, 0 otherwise (evaluated each k-cycle)

## Example

```csound
<Cabbage>[
    {"type":"form","caption":"Simple Instrument","size":{"width":600,"height":300},"pluginId":"HKey"},
    {"type":"rotarySlider","channel":"gain","bounds":{"left":100,"top":50,"width":100,"height":100},"range":{"min":0,"max":1,"value":0.5},"text":"Gain"}
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
    ; Check if the "gain" widget has a "range" property
    iHasRange = cabbageHasKey("gain", "range")
    if iHasRange == 1 then
        prints("gain widget has a range property\n")
    endif

    ; Check for a nested property using dot-notation
    iHasMin = cabbageHasKey("gain", "range.min")
    if iHasMin == 1 then
        prints("gain widget has range.min property\n")
    endif

    ; Check for a property that doesn't exist
    iHasFoo = cabbageHasKey("gain", "foo")
    if iHasFoo == 0 then
        prints("gain widget does not have a foo property\n")
    endif
endin

</CsInstruments>
<CsScore>
i1 0 z
</CsScore>
</CsoundSynthesizer>
```

## Notes

- If the specified channel does not match any widget, 0 is returned.
- Dot-notation traverses nested JSON objects, so `"bounds.left"` checks that both `bounds` and `left` within it exist.

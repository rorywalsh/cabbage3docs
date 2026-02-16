# cabbageDump

This opcode will print the JSON representation of a widget to the Csound console. This can be useful for debugging widgets.

## Syntax
```js
cabbageDump:i(SChannel, iIndent)
cabbageDump:k(kTrig, SChannel, iIndent)
```

### Initialization
* *SChannel* – the name of the channel to query
* *iIndent* - If *iIndent* is nonnegative, then array elements and object members will be pretty-printed with that indent level. An indent level of 0 will only insert newlines. -1 selects the most compact representation. The default level is 4.

### Performance
* *kTrig* - a trigger signal that will cause the widget's JSON representation to be printed to the console.

## Example:

```cs
<Cabbage>[
    {"type":"form","caption":"Simple Instrument","size":{"width":1000,"height":520},"pluginId":"RMSy"},
    {"type":"rotarySlider", "channel":"gain", "bounds":{"left":150, "top":10, "width":100, "height":100}, "range":{"min":0, "max":2, "value":1, "skew":1, "increment":0.1}, "text":"Gain"},
]
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-dm0 -n -+rtmidi=NULL -M0 --midi-key=4 --midi-velocity=5
</CsOptions>
<CsInstruments>
; sr set by host
ksmps = 16
nchnls = 2
0dbfs = 1

instr 1 
    //print entire JSON object associated with 'gain' widget
    cabbageDump "gain", 4
endin

</CsInstruments>  
<CsScore>
i1 0 1
</CsScore>
</CsoundSynthesizer>
```

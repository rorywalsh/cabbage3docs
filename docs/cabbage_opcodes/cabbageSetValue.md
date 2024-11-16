# CabbageSetValue

This opcode set the current value of a widget. It can run at init-time or k-time. 

## Syntax

**cabbageSetValue** *SChannel*, *kValue* 
**cabbageSetValue** *SChannel*, *iValue* 


### Initialization
* *SChannel* – the name of the channel to query
* *iValue* - the value to set the widget too

### Performance
* *kValue* - the value to set the widget too


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
    kSliderValue, kTrig cabbageGetValue "gain"
    //print value of 'gain' slider each time its updated
    printf "Value of %s widget is now %f", kTrig, kSliderValue
endin

</CsInstruments>  
<CsScore>
i1 0 z
</CsScore>
</CsoundSynthesizer>
```

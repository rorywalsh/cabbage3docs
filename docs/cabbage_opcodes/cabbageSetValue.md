import CodeBlock from '@theme/CodeBlock';
import widgetCode from '!!raw-loader!../../static/examples/cabbageSet.csd';

# cabbageSetValue

This opcode sets the current value of a widget and can be executed at either init-time or k-time. When called, it immediately writes the incoming value to a Csound channel and also places the value into a FIFO queue, which the frontend reads to update the UI.

Because the frontend operates at a much lower frame rate than the audio thread, it cannot process every value update. While all updates are written to the underlying Csound channel, many intermediate values will not make it into the FIFO queue and therefore will not be seen by the frontend. However, the most recent value will always make it through, ensuring the UI remains in sync with the latest state.

## Syntax
```js
cabbageSetValue:k(SChannel, kValue [, kTrigger]) 
cabbageSetValue:i(SChannel, iValue) 
```

### Initialization
* *SChannel* – the name of the channel to query
* *iValue* - the value to set the widget too

### Performance
* *kValue* - the value to set the widget too
* *kTrigger* - a signal used to trigger a value update 


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

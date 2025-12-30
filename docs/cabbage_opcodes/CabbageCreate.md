# CabbageCreate

This opcode will create a new widget based on a JSON object. Note that widgets generated in this way cannot be registered as parameters. This means they cannot be automated by the host.  

## Syntax

**cabbageCreate** *SJson*

### Initialization
* *SJson* – a well-formed JSON string. This will typically look like a JSON object from the Cabbage section JSON array.
 
> Note you need to provide a channel and a valid type when creating the string.  


## Example:

```cs
<Cabbage>
[
    {"type": "form", "caption": "Template Effect", "size": {"width": 580, "height": 300}, "pluginId": "def1"},
    {
        "type": "image",
        "id": "scrubber",
        "bounds": {"left": 9, "top": 9, "width": 32, "height": 278},
        "channels": [{"id": "image130", "range": {"increment": 0.001}}],
        "style": {"backgroundColor": "#0295cffd"},
        "zIndex": -1
    }
]
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d
</CsOptions>
<CsInstruments>
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    x:i, y:i init 0
    widgetCount:i init 0
    while y < 8 do
        while x < 16 do
            SWidget = sprintf({{
            {
            "type": "checkBox",
            "bounds":{"left":%d, "top":%d, "width":30, "height":30},
            "channels": [{"id": "check%d"}],
            "style": {
            "on": {"backgroundColor": "#ffa71e"},
            "off": {"backgroundColor": "#d5d5d5ff"}
            },
            "automatable":false
            }
            }}, 10+x*35, 10+y*35, widgetCount)
            cabbageCreate(SWidget)
            widgetCount += 1
            x += 1
        od
        x = 0
        y += 1
    od
    
    column:k init 0
    scrubberPos:k init 0
    numRows:i = 8
    numCols:i = 16
    
    if metro(2)==1 then
        row:k = 0
        while row<numRows do
            checkNum:k = column + row*numCols
            val:k = cabbageGetValue(sprintfk("check%d", checkNum))
            if val == 1 then
                event("i", "Synth", 0, 1, ((8-row)+10)*10, .3)
            endif
            row = row+1
        od
        cabbageSet(1, "scrubber", "bounds.left", (column*35+9))
        column = (column+1) % numCols
    endif
endin

instr Synth
    aEnv = expon(p5, p3, 0.01)
    aOut = oscil(aEnv, p4)
    outs(aOut, aOut)
endin

</CsInstruments>
<CsScore>
f1 0 4096 10 1 .5 .25 .17
i1 0 z
</CsScore>
</CsoundSynthesizer>
```

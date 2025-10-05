<Cabbage>[
{"type": "form", "caption": "XyPad Example", "size": {"width": 520, "height": 520}, "pluginId": "xyp1"},
{"type": "xyPad", "bounds": {"left": 10, "top": 10, "width": 250, "height": 250}, "channel": {"id": "xyPad1", "x": "cutoff", "y": "resonance"}, "range": {"x": {"min": 100, "max": 10000, "defaultValue": 1000, "skew": 0.5, "increment": 1}, "y": {"min": 0.1, "max": 20, "defaultValue": 5, "skew": 1, "increment": 0.1}}, "text": {"x": "Cutoff", "y": "Resonance"}, "ballSize": 20, "corners": 5},
{"type": "xyPad", "bounds": {"left": 270, "top": 10, "width": 240, "height": 240}, "channel": {"id": "xyPad2", "x": "freq", "y": "amp"}, "range": {"x": {"min": 200, "max": 2000, "defaultValue": 440, "skew": 1, "increment": 1}, "y": {"min": 0, "max": 1, "defaultValue": 0.5, "skew": 1, "increment": 0.01}}, "text": {"x": "Frequency", "y": "Amplitude"}, "ballSize": 25, "colour": {"fill": "#1a1a2e", "ball": {"fill": "#ff6b6b"}}, "corners": 8},
{"type": "xyPad", "bounds": {"left": 10, "top": 270, "width": 240, "height": 240}, "channel": {"id": "xyPad3", "x": "pan", "y": "reverb"}, "range": {"x": {"min": 0, "max": 1, "defaultValue": 0.5, "skew": 1, "increment": 0.01}, "y": {"min": 0, "max": 1, "defaultValue": 0.3, "skew": 1, "increment": 0.01}}, "text": {"x": "Pan", "y": "Reverb"}, "ballSize": 18, "colour": {"fill": "#2d2d44", "ball": {"fill": "#4ecdc4"}}}
]
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-n -d -+rtmidi=NULL -M0 -m0d 
</CsOptions>
<CsInstruments>
; Initialize the global variables. 
ksmps = 32
nchnls = 2
0dbfs = 1

; Rory Walsh 2021 
;
; License: CC0 1.0 Universal
; You can copy, modify, and distribute this file, 
; even for commercial purposes, all without asking permission. 

instr 1
    ; Get X-Y values from the first xyPad
    kCutoff cabbageGetValue "cutoff"
    kResonance cabbageGetValue "resonance"
    
    ; Get X-Y values from the second xyPad
    kFreq cabbageGetValue "freq"
    kAmp cabbageGetValue "amp"
    
    ; Get X-Y values from the third xyPad
    kPan cabbageGetValue "pan"
    kReverb cabbageGetValue "reverb"
    
    ; Generate a simple oscillator
    aOsc oscili kAmp * 0.3, kFreq
    
    ; Apply resonant filter using xyPad1 values
    aFilt reson aOsc, kCutoff, kResonance, 2
    
    ; Simple reverb
    aRvbL, aRvbR reverbsc aFilt, aFilt, kReverb, 8000
    
    ; Mix dry and reverb signals
    aMix = aFilt * (1 - kReverb * 0.5) + (aRvbL + aRvbR) * 0.5 * kReverb
    
    ; Pan the signal
    aLeft = aMix * sqrt(1 - kPan)
    aRight = aMix * sqrt(kPan)
    
    outs aLeft, aRight
endin

</CsInstruments>
<CsScore>
;starts instrument 1 and runs it for a week
i1 0 z
</CsScore>
</CsoundSynthesizer>

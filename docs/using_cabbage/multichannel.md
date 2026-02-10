---
title: Working with Multichannel Instruments
description: Managing multichannel setups
---


While any instrument that processes more than one signal channel can be considered multichannel, the term is typically used for instruments that handle more than two channels.

### Defining number of outputs 

The number of outputs can be specified in the Csound header section using the nchnls keyword, which indicates how many output channels the instrument should use. In the following setup, the instrument is configured with two outputs.

```js
<CsoundSynthesizer>
<CsOptions>
-n -d -+rtmidi=NULL -M0 -m0d 
</CsOptions>
<CsInstruments>
ksmps = 32
nchnls = 2 //stereo output 
0dbfs = 1
```

### Defining the number of inputs

Similarly, we can use the `nchnls_i` keyword to set the number of input channels. 

```
<CsoundSynthesizer>
<CsOptions>
-n -d -+rtmidi=NULL -M0 -m0d 
</CsOptions>
<CsInstruments>
ksmps = 32
nchnls = 2      //stereo output 
nchnls_i = 4    //quadraphonic input
0dbfs = 1
```

📃 **Note:**  The numer given for `nchnls` will be taken as the number of input channels *if* `nchnls_i` is not defined. 

## Instruments with side-chains 

A sidechain channel in audio processing is an auxiliary input that influences how a plugin or processor (e.g., a compressor or gate) behaves. Instead of relying solely on the main audio input, the plugin uses the sidechain input as a control signal to guide its processing. In Cabbage terms, this is typically an instrument with more inputs than outputs. For example the following instrument might use the first 2 input channels to process the main stereo input, and the third input channel to control a gate.

```
<CsoundSynthesizer>
<CsOptions>
-n -d -+rtmidi=NULL -M0 -m0d 
</CsOptions>
<CsInstruments>
ksmps = 32
nchnls = 2      //stereo output 
nchnls_i = 3    //stereo plus mono input
0dbfs = 1
```


## Buses

An audio bus is a logical grouping of audio channels that allows for the routing and processing of multiple audio signals as a single unit. Buses are used to simplify signal management, enabling plugins to handle mono, stereo, surround, or custom configurations seamlessly and integrate effectively with the DAW's mixing and routing workflows. Sidechaining is typically handled using a unique bus. 

In order to set up custom busing in Cabbage 3 we define a list of available bus configurations in our `form` widget. For this we use the `channelConfig` property, which can be assigned a string with all supported configurations. In the case of our simple sidechain setup from above, we should probably group the inputs into a stereo bus, and the sidechain channel into a mono bus. To do this we add '2.1-2' to our `chanelConfig` property. 

```
{
    "type": "form",
    "caption": "Effect",
    "size": {
        "height": 300,
        "width": 580
    },
    "pluginId": "def1",
    "channelConfig":"2.1-2, 2-2, 1-1"
}
```

Any number of bus arrangements can be specified, but they must conform to the total number of inputs and outputs defined in the Csound header section.

Some hosts may override the requested bus or channel configuration. For example, dropping an instrument with `nchnls=2` onto a mono track in Logic will cause Logic to change the configuration to mono. In this case, Cabbage will overwrite `nchnls` and set it to 1. It is therefore recommended to use code like the following in instruments:

```js
if (nchnls == 1) then
    outs (aLeft+aRight)/2
else
    outs (aLeft, aRight)
endif
```

This will prevent Csound from trying to access an input or output channel that is not available.  
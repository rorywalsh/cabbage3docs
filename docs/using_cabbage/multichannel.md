---
title: Working with Multichannel Instruments
description: Managing multichannel setups
---


While any instrument that processes more than a signal channels can be classified as multichannel, the term is typically reserved for instruments that process more than 2 channels. 

### Defining number of outputs 

We can define the number of outputs we would like in our Csound header section. We can use the `nchnls` keyword to tell Csound how many output channels to use. In the following setup the instrument will have 2 outputs. 

```
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

> Note that `nchnls` will be taken as the number of input channels if `nchnls_i` is not defined. 

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

You can specify as many bus arranges as you like, but they must adhere to the overall number of inputs and outputs you set in your Csound header section. 

Note that some hosts may try to override, `nchnls/nchnls_i`. For example, if you drop an instrument with `nchnls=2` defined onto a mono track in Logic, `nchnls` will be overwritten and set to 1. That’s why it’s a good idea to use code like this in your instruments:

```
if nchnls == 1 then
    outs (aLeft+aRight)/2
else
	outs aLeft, aRight
endif
```

This will prevent Csound from trying to access an input or output channel that is not available.  
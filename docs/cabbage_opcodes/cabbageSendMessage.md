# cabbageSendMessage

This opcode sends arbitrary JSON data directly to the frontend, allowing you to create custom messages for specialized UI interactions or data visualization. Unlike other Cabbage opcodes that update specific widget properties, `cabbageSendMessage` gives you complete control over the message format and content.

📃 **Note:** Every message sent via `cabbageSendMessage` is added to a queue that is passed to the frontend. Calling `cabbageSendMessage` at k-rate can generate a high volume of messages, which may clog the communication channels between Csound and the plugin UI. Therefore, care must be taken to send messages only when absolutely necessary. 

The JSON message is sent as-is to the frontend, where it can be handled by custom JavaScript code. This is particularly useful for:
- Sending arrays of data for custom visualizations
- Triggering custom frontend behaviors
- Sending complex data structures that don't map to standard widget properties
- Implementing custom communication protocols between Csound and your UI

## Syntax
```js
cabbageSendMessage:i(SJsonString)
cabbageSendMessage:k(kTrigger, SJsonString)
```
### Initialization
* *SJsonString* – a valid JSON string (object or array) to send to the frontend

### Performance
* *kTrigger* - a signal used to trigger sending the message (sends when trigger == 1)
* *SJsonString* – a valid JSON string (object or array) to send to the frontend

## Important Notes

- The JSON string must be valid JSON syntax. Invalid JSON will generate a Csound error.
- Messages are sent through the same queue system as widget updates.
- The frontend is responsible for handling and interpreting these messages.
- Messages bypass the channel cache system and are sent directly to the UI queue.

## Example:

### Sending Custom Data Arrays

```cs
<Cabbage>[
    {"type":"form","caption":"Custom Message Demo","size":{"width":800,"height":400},"pluginId":"CMsg"}
]
</Cabbage>
<CsoundSynthesizer>
<CsOptions>
-dm0 -n
</CsOptions>
<CsInstruments>
ksmps = 64
nchnls = 2
0dbfs = 1

; Send a message at init time
instr 1
    ; Send a simple status message
    SJson = sprintf(R{"type":"status","message":"Instrument initialized"}R)
    cabbageSendMessage(SJson)
endin

; Send periodic updates at k-rate
instr 2
    trig:k = metro(4)  ; Update 4 times per second

    ; Build JSON message with current values
    SJson  = sprintf(R{"type":"dataUpdate","value":%d"}R, random:k(0, 100))

    ; Send when triggered
    cabbageSendMessage kMetro, SJson
endin


</CsInstruments>
<CsScore>
i1 0 1      ; Send init message
i2 0 10     ; Send periodic updates for 10 seconds
</CsScore>
</CsoundSynthesizer>
```

### Frontend Handling (JavaScript)

To receive and handle these custom messages in your frontend code:

```javascript
// In your custom widget or frontend code
Cabbage.addMessageListener((message) => {
    // The message is the JSON object sent from Csound
    if (message.type === "status") {
        console.log("Status:", message.message);
    }
    else if (message.type === "dataUpdate") {
        updateVisualization(message.phase, message.value);
    }
    else if (message.type === "spectrum") {
        drawSpectrum(message.data);
    }
});
```

## Use Cases

1. **Real-time Data Visualization**: Send arrays of FFT data, waveform samples, or other analysis results for custom visualization.

2. **State Synchronization**: Broadcast complex state changes that involve multiple related values.

3. **Event Notifications**: Trigger frontend animations, transitions, or other visual effects based on musical events.

4. **Custom Protocols**: Implement domain-specific communication between Csound instruments and specialized UI components.


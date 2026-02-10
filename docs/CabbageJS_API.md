---
title: Cabbage JS API
description: Cabbage API
---

# Cabbage JavaScript API Reference

The Cabbage JavaScript API provides the communication layer between webview UIs and the Cabbage backend. This API enables bidirectional communication for plugin development. 

📃 **Note:** A `<Cabbage>{...}</Cabbage>` JSON structure is still required to define parameters for use in a host application. Objects declared in this structure are accessible through the API via a custom event handler (see below). These objects are sent at load time and can be updated at runtime using the [`cabbageSet`](/docs/cabbage_opcodes/cabbageSet) and [`cabbageSetValue`](/docs/cabbage_opcodes/cabbageSetValue) opcodes.

## Architecture Overview

### UI → Backend (Outgoing Communication)
Use `Cabbage.sendControlData()` to send widget value changes to the backend. The backend automatically determines routing based on channel automatable status.

### Backend → UI (Incoming Communication)
The backend sends messages via `window.hostMessageCallback()`. Implement this global function to handle incoming messages.

## API Reference

### Core Functions

#### `Cabbage.sendControlData(data, vscode)`

Send widget value changes to the Cabbage backend. This is the primary API for user interactions.

**Parameters:**
- `data` (Object): Control data object
  - `channel` (string): The channel name
  - `value` (number|string): Value in natural range (e.g., 20-20000 Hz for frequency)
  - `gesture` (string, optional): Gesture type - `"begin"`, `"value"`, `"end"`, `"complete"` (default: `"complete"`)
- `vscode` (Object|null): VS Code API instance (null for plugin mode)

**Behavior:**
- Automatically routes based on channel automatable status
- Thread-safe: Asynchronous, doesn't block audio thread
- Values sent in natural ranges, backend handles normalization

**Examples:**
```javascript
// Basic usage
Cabbage.sendControlData({ channel: "frequency", value: 1000 }, this.vscode);

// With gesture for DAW automation
Cabbage.sendControlData({ channel: "volume", value: 0.8, gesture: "begin" }, this.vscode);
Cabbage.sendControlData({ channel: "volume", value: 0.9, gesture: "value" }, this.vscode);
Cabbage.sendControlData({ channel: "volume", value: 0.9, gesture: "end" }, this.vscode);
```

---

#### `Cabbage.sendChannelData(channel, data, vscode)`

Send channel data directly to Csound without DAW automation - bypasses all widget routing and validation. 

**Parameters:**
- `channel` (string): Csound channel name
- `data` (number|string): Data to send
- `vscode` (Object|null): VS Code API instance

**Notes:**
- Use `sendControlData()` instead for most cases as it will determine the best route for this data
- Bypasses DAW automation system
- Automatically determines string vs numeric data


---

#### `Cabbage.sendMidiMessageFromUI(statusByte, dataByte1, dataByte2, vscode)`

Send MIDI messages from the UI to the backend.

**Parameters:**
- `statusByte` (number): MIDI status byte
- `dataByte1` (number): First data byte
- `dataByte2` (number): Second data byte
- `vscode` (Object|null): VS Code API instance

**Example:**
```javascript
Cabbage.sendMidiMessageFromUI(144, 60, 100, this.vscode); // Note on
```

---

#### `Cabbage.MidiMessageFromHost(statusByte, dataByte1, dataByte2)`

Handle incoming MIDI messages from the backend (callback function).

**Parameters:**
- `statusByte` (number): MIDI status byte
- `dataByte1` (number): First data byte
- `dataByte2` (number): Second data byte


---

#### `Cabbage.isReadyToLoad(vscode, additionalData)`

Signal that the UI is ready to load and initialize.

**Parameters:**
- `vscode` (Object|null): VS Code API instance
- `additionalData` (Object, optional): Additional initialization data

### Utility Functions

---

#### `Cabbage.triggerFileOpenDialog(vscode, channel, options)`

Trigger a file open dialog for file selection widgets.

**Parameters:**
- `vscode` (Object|null): VS Code API instance
- `channel` (string): Associated channel name
- `options` (Object, optional): Dialog options
  - `directory` (string): Starting directory
  - `filters` (string): File filters
  - `openAtLastKnownLocation` (boolean): Use last known location

**Example:**
```javascript
Cabbage.triggerFileOpenDialog(this.vscode, "audioFile", {
    filters: "*.wav;*.aiff",
    openAtLastKnownLocation: true
});
```

---

#### `Cabbage.openUrl(vscode, url, file)`

Open a URL or file in the system default application.

**Parameters:**
- `vscode` (Object|null): VS Code API instance
- `url` (string): URL to open
- `file` (string): File path to open

#### `Cabbage.requestResize(width, height, vscode)`

Request a resize of the plugin GUI window (plugin mode only).

**Parameters:**
- `width` (number): Requested width in pixels
- `height` (number): Requested height in pixels
- `vscode` (Object|null): VS Code API instance

**Notes:**
- Only works in plugin mode (CLAP/VST3/AUv2)
- Host may accept or reject the request
- Backend sends a `resizeResponse` message indicating acceptance and final dimensions


### Private Functions 

⚠️ **Important:** These functions are used internally and are not for general use.  

#### `Cabbage.sendCustomCommand(command, vscode, additionalData)`

Send custom commands to the backend for specialized operations.

**Parameters:**
- `command` (string): Command name
- `vscode` (Object|null): VS Code API instance
- `additionalData` (Object, optional): Additional data to send

**Example:**
```javascript
Cabbage.sendCustomCommand('cabbageIsReadyToLoad', null);
```

---

#### `Cabbage.sendWidgetUpdate(widget, vscode)`

Update widget state in the backend (used by property panel).

**Parameters:**
- `widget` (Object): Widget configuration object
- `vscode` (Object|null): VS Code API instance


---

## Incoming Messages (Backend -> UI)

Implement `window.hostMessageCallback` to handle messages from the backend:

```javascript
window.hostMessageCallback = function(data) {
    switch(data.command) {
        case "parameterChange":
            // DAW automation or backend parameter update
            // Update display only - NEVER send back to backend
            // updateWidgetDisplay(data.channel, data.value);
            break;

        case "updateWidget":
            // Widget property update from Csound (cabbageSetValue, cabbageSet)
            // updateWidget(data.widgetJson);
            break;

        case "csoundOutputUpdate":
            // Csound console output for debugging
            console.log("Csound output:", data.text);
            break;

        case "resizeResponse":
            // Response to GUI resize request
            if (data.accepted) {
            //     updateGuiDimensions(data.width, data.height);
            } else {
            //     handleResizeRejected(data.width, data.height);
            }
            break;
    }
};
```

### Message Types

#### `parameterChange`
- **Purpose**: Parameter updates from DAW automation or backend
- **Fields**: `channel`, `value`, `gesture`
- **Action**: Update visual display only (avoid feedback loops)

---

#### `updateWidget`
- **Purpose**: Widget state updates from Csound opcodes
- **Fields**: `id`, `widgetJson`, `value` (optional)
- **Action**: Update widget properties and visual state

---

#### `csoundOutputUpdate`
- **Purpose**: Csound console output for debugging
- **Fields**: `text`
- **Action**: Display or log Csound output

---

#### `resizeResponse`
- **Purpose**: Response to GUI resize requests
- **Fields**: `accepted` (boolean), `width` (number), `height` (number)
- **Action**: Handle resize acceptance/rejection and update UI dimensions

---

## Gesture Types

Use appropriate gestures for proper DAW automation recording:

- **`"begin"`**: Start of user interaction (e.g., mouse down on slider)
- **`"value"`**: Continuous updates during interaction (e.g., mouse drag)
- **`"end"`**: End of continuous interaction (e.g., mouse up)
- **`"complete"`**: Discrete actions (e.g., button clicks, default)


## Best Practices

### Avoiding Feedback Loops
When receiving `parameterChange` messages, **only update the visual display**. Never send `sendControlData()` in response, as this creates feedback loops that interfere with DAW automation.

### Thread Safety
All outgoing functions are asynchronous and thread-safe. They queue messages without blocking the audio thread.

### Value Ranges
Send values in their full/natural ranges (e.g., 20-20000 Hz for frequency). The backend handles all DAW normalization automatically.

### Environment Detection
- **VS Code mode**: Pass `this.vscode` as the vscode parameter
- **Plugin mode**: Pass `null` for vscode parameter
- Functions automatically detect the environment and use appropriate communication channels


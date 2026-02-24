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
Use `Cabbage.addMessageListener(callback)` to receive messages from the backend. This works in all environments — VS Code, native DAW plugins, and custom UI frameworks — without any environment-specific setup.

## API Reference

### Core Functions

#### `Cabbage.addMessageListener(callback)`

Register a listener for incoming messages from the Cabbage backend. This is the recommended way to handle all backend → UI communication. It abstracts the two runtime environments so that the same UI code works everywhere:

- **VS Code (custom UI / iframe relay)**: messages arrive as `window` message events
- **Native plugin (DAW)**: messages arrive via `window.hostMessageCallback`

**Parameters:**
- `callback` (function): Called with each incoming message object

**Returns:** A cleanup function — call it when the UI is torn down to avoid memory leaks.

**Incoming message shapes:**

| `command` | Fields | Sent by |
|-----------|--------|---------|
| `parameterChange` | `paramIdx`, `value` (may be top-level or nested in `data`) | DAW automation / backend |
| `widgetUpdate` | `id`, `value` | [`cabbageSetValue`](/docs/cabbage_opcodes/cabbageSetValue) opcode |
| `widgetUpdate` | `id`, `widgetJson` | [`cabbageSet`](/docs/cabbage_opcodes/cabbageSet) opcode |
| `channelDataUpdate` | `channel`, `value` | Csound channel data |
| `resizeResponse` | `accepted`, `width`, `height` | Response to `requestResize()` |

**Example — Vanilla HTML:**
```javascript
import { Cabbage } from './cabbage/cabbage.js';

Cabbage.addMessageListener((msg) => {
    if (msg.command === 'parameterChange') {
        // paramIdx/value may be top-level or nested in msg.data (DAW host dependent)
        const data = msg.data ?? msg;
        updateSlider(data.paramIdx, data.value);
    } else if (msg.command === 'widgetUpdate') {
        // id and value are always top-level
        if (msg.value !== undefined) {
            document.getElementById(msg.id).value = msg.value;
        } else if (msg.widgetJson !== undefined) {
            const widget = JSON.parse(msg.widgetJson);
            // apply full widget update...
        }
    }
});
```

**Example — Svelte:**
```javascript
import { Cabbage } from 'cabbage';
import { onMount, onDestroy } from 'svelte';

let removeListener;

onMount(() => {
    removeListener = Cabbage.addMessageListener((msg) => {
        if (msg.command === 'widgetUpdate' && msg.id === 'myChannel') {
            myValue = msg.value;
        }
    });
});

onDestroy(() => removeListener?.());
```

---

#### `Cabbage.sendControlData(data, vscode)`

Send widget value changes to the Cabbage backend. This is the primary API for user interactions.

**Parameters:**
- `data` (Object): Control data object
  - `channel` (string): The channel name
  - `value` (number|string): Value in natural range (e.g., 20-20000 Hz for frequency)
  - `gesture` (string, optional): Gesture type - `"begin"`, `"value"`, `"end"`, `"complete"` (default: `"complete"`)
- `vscode` (Object|null): VS Code API instance (pass `null` for plugin mode)

**Behavior:**
- Automatically routes based on channel automatable status
- Thread-safe: Asynchronous, doesn't block audio thread
- Values sent in natural ranges, backend handles normalization

**Examples:**
```javascript
// Basic usage
Cabbage.sendControlData({ channel: "frequency", value: 1000 }, null);

// With gesture for DAW automation recording
Cabbage.sendControlData({ channel: "volume", value: 0.8, gesture: "begin" }, null);
Cabbage.sendControlData({ channel: "volume", value: 0.9, gesture: "value" }, null);
Cabbage.sendControlData({ channel: "volume", value: 0.9, gesture: "end" }, null);
```

---

#### `Cabbage.sendChannelData(channel, data, vscode)`

Send channel data directly to Csound without DAW automation — bypasses all widget routing and validation.

**Parameters:**
- `channel` (string): Csound channel name
- `data` (number|string): Data to send
- `vscode` (Object|null): VS Code API instance

**Notes:**
- Use `sendControlData()` instead for most cases as it determines the best route automatically
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
Cabbage.sendMidiMessageFromUI(144, 60, 100, null); // Note on
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
Cabbage.triggerFileOpenDialog(null, "audioFile", {
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

---

#### `Cabbage.consumeKeypresses(consume)` *(Windows plugin mode only)*

Control whether keyboard events are captured by the webview or forwarded to the host DAW.

By default (`false`), all key events are passed through to the DAW so keyboard shortcuts keep working while the plugin UI has focus. This is handled automatically by Cabbage's internal key listener.

**Parameters:**
- `consume` (boolean): `true` to capture keys in the webview, `false` to pass them through to the DAW (default)

**Notes:**
- Native `<input>` and `<textarea>` elements are handled automatically — no need to call this
- Only required for custom text-entry widgets built from non-native elements (e.g. a `div`-based code editor)
- Always restore to `false` when the custom widget loses focus

**Example:**
```javascript
myCustomEditor.addEventListener('focus', () => Cabbage.consumeKeypresses(true));
myCustomEditor.addEventListener('blur',  () => Cabbage.consumeKeypresses(false));
```

---

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

## Incoming Messages (Backend → UI)

Use `Cabbage.addMessageListener()` to handle all incoming messages. See [the full API entry above](#cabbageaddmessagelistenercallback) for details and examples.

### Message Types

#### `parameterChange`
- **Purpose**: Parameter updates from DAW automation or backend
- **Fields**: `paramIdx`, `value` — may be top-level or nested inside `data` depending on the host
- **Action**: Update visual display only — **never** call `sendControlData()` in response (causes feedback loops)

---

#### `widgetUpdate`
- **Purpose**: Widget value or property update from Csound opcodes (`cabbageSetValue`, `cabbageSet`)
- **Fields**: `id` (string), and either `value` (number) for simple updates or `widgetJson` (string) for full property updates
- **Action**: Update the corresponding widget's value or properties

---

#### `channelDataUpdate`
- **Purpose**: Channel data from Csound
- **Fields**: `channel`, `value`

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
When receiving `parameterChange` messages, **only update the visual display**. Never call `sendControlData()` in response, as this creates feedback loops that interfere with DAW automation.

### isDragging Pattern
When a user is actively dragging a slider, ignore incoming `parameterChange` updates to prevent the UI fighting with the user's input:

```javascript
let isDragging = false;

slider.addEventListener('pointerdown', () => { isDragging = true; });
slider.addEventListener('pointerup',   () => { isDragging = false; });

Cabbage.addMessageListener((msg) => {
    if (msg.command === 'parameterChange' && !isDragging) {
        const data = msg.data ?? msg;
        slider.value = data.value;
    }
});
```

### Thread Safety
All outgoing functions are asynchronous and thread-safe. They queue messages without blocking the audio thread.

### Value Ranges
Send values in their full/natural ranges (e.g., 20-20000 Hz for frequency). The backend handles all DAW normalization automatically.

### Environment Detection
Pass `null` for the `vscode` parameter in all API calls — the library detects the environment automatically. The `vscode` parameter is a legacy option retained for backwards compatibility with older custom UIs that acquired the VS Code API directly.

---
title: Custom Widgets
description: Creating custom widget classes for use with the Cabbage editor
---

# Custom Widgets

Creating custom widget classes allows you to develop new controls while retaining the full editing tools provided by the Cabbage VS Code extension — including the property panel and drag-to-position editing. New widgets can be created using the command palette by selecting **Create New Custom Widget**.

If a custom widget folder does not already exist, the extension will prompt for its creation and automatically copy the required files into it. These files are placed inside a `src` directory, which must not be moved.

Custom widget classes must be placed in the `widgets` subdirectory within `src`, i.e. `CustomWidgetFolder/src/widgets`. This ensures that the extension can locate and load them via the property panel. The file name also serves as the class name.

📃 **Note:** The custom widget folder must contain a top-level `cabbage` directory (i.e. the directory that contains the `widgets` subfolder). Maintaining this structure ensures that all paths are correctly resolved by Cabbage.

By convention, Cabbage classes use *UpperCamelCase*, while widget types use lowerCamelCase. The backend handles all value normalization required by the host DAW, allowing frontends to send and receive values in their full ranges (e.g., 20–20000 Hz for filter frequency, rather than normalized 0.0–1.0 values).

## Required Interface

For a widget to be recognized by the Cabbage VS Code extension — particularly by the property panel — it must implement the following:

### `this.props`

A JSON object containing properties accessible through the UI element inspectors in VS Code. Any property defined here can also be queried and modified using the Cabbage get and set opcodes in Csound. Properties can be objects, strings, or numbers. Boolean can be used only for set Cabbage properties such as `visible`, `active`, `automatable`, etc. Use 0/1 if you need to send boolean values to the backend.

At a minimum, the props object must include:
- An `id` property
- A `channels` array
- An `automatable` property (boolean)
- A `bounds` object to define dimensions and placement
- A `vscode` property (assigned to the VS Code API instance when running from VS Code, undefined otherwise)
- A `zIndex` property (integer)
- A `visible` property (boolean)
- An `active` property (boolean)

### Event Listener Methods

- **`addVsCodeEventListeners(widgetDiv, vs)`**: Called when Cabbage is running from VS Code. Initialise your vscode API instance here.
- **`addEventListeners()`**: Called when Cabbage is running as a plugin.

Both methods need to be implemented to ensure compatibility with different environments. The simplest pattern is to put all the event handler code into `addEventListener()`, and then call it from `addVsCodeEventListeners()`.

### `getInnerHTML()`

Returns the inner HTML used to render the UI element. The element's size is determined by its `bounds` object. You can return an SVG element or a `div`, depending on your design. The `WidgetManager` class calls this method when the widget is first inserted (via `insertWidget()`) and whenever properties change (via `updateWidget()`).

For canvas-based widgets, `getInnerHTML()` is called during insertion to create the initial DOM structure, but subsequent updates use `updateCanvas()` instead to avoid destroying the canvas context.

### `createCanvas()` and `updateCanvas()` *(canvas widgets only)*

If you need a canvas for drawing, add a `createCanvas()` function that initialises the canvas and an `updateCanvas()` function that updates its contents. These are called by the `WidgetManager` to manage the embedded graphics context.

### Reactive Properties *(optional)*

If you need to listen for changes to widget properties, wrap `this.props` with `CabbageUtils.createReactiveProps()`. This creates a Proxy that automatically handles common widget behaviours (like toggling pointer-events when `visible` or `active` change) and can notify you of property changes. Call it in your constructor:

```javascript
this.props = CabbageUtils.createReactiveProps(this, this.props, {
    onPropertyChange: (change) => {
        // change.key      - the property name
        // change.value    - new value
        // change.oldValue - previous value
        // change.path     - dot-separated path to the property
    },
    watchKeys: null,   // null = watch all, or array of strings/RegExp
    mode: 'change',    // 'change' = only notify when value differs, 'set' = notify on every set
    lazyPath: true     // compute path only when notifying (more efficient)
});
```

The `opts` parameter is optional — you can call `CabbageUtils.createReactiveProps(this, this.props)` without options for basic reactive behaviour.

> **Performance Note**: Don't use `onPropertyChange` to listen for `value` updates from Csound resulting from calls to `cabbageSetValue`. The `WidgetManager` automatically calls `updateCanvas()` for canvas-based widgets when channel values change, bypassing the reactive props system for efficiency. Value updates are sent as lightweight messages without full widget JSON, allowing high-frequency updates (e.g., for k-rate parameter changes) without overhead. Use reactive props for UI-driven property changes (like `visible`, `bounds`, or custom properties), not for high-frequency value streams.

## Sending Data to the Backend

To send data from your widget to the Cabbage backend, use `Cabbage.sendControlData()`:

```javascript
Cabbage.sendControlData({ channel: "myChannel", value: 42, gesture: "complete" }, this.vscode);
```

**Parameters:**
- `channel`: The channel name (string)
- `value`: The value in its natural range (e.g., 20–20000 Hz for filter frequency)
- `gesture`: Optional — `"begin"`, `"value"`, `"end"`, or `"complete"` (default)
- `vscode`: The VS Code API instance (`this.vscode` in your widget; safely ignored as a plugin)

The backend automatically determines whether the channel is automatable and routes accordingly. For non-automatable data you can also call `sendChannelData()` directly:

```javascript
Cabbage.sendChannelData("myStringChannel", "hello", this.vscode);
Cabbage.sendChannelData("myNumberChannel", 3.14, this.vscode);
```

## Channel Communication

The `channels` array defines the channels used to send value updates from the front end to the back end. If no `this.props.id` is defined, the first `channel.id` in the array is used as the primary DOM identifier.

For multi-channel widgets (like an EQ controller with separate frequency and gain channels per band), the `WidgetManager` automatically routes incoming parameter updates to the correct channel based on the channel ID. Each channel should have:
- `id`: Unique channel identifier
- `range`: Object with `min`, `max`, `defaultValue`, and optionally `value`
- `event`: Optional event type (e.g., `"valueChanged"`, `"mouseDragX"`, `"mouseDragY"`)

## CabbageUtils Helper Functions

#### `CabbageUtils.getWidgetDivId(props)`
Returns the DOM ID for the widget's div element. Prioritises `props.id`, then falls back to `channels[0].id`.

```javascript
const divId = CabbageUtils.getWidgetDivId(this.props);
```

#### `CabbageUtils.getWidgetDiv(channelOrProps)`
Returns the actual DOM element for the widget div. Accepts either a props object or a string div ID. Returns `null` if not found.

```javascript
const widgetDiv = CabbageUtils.getWidgetDiv(this.props);
const widgetDiv = CabbageUtils.getWidgetDiv("myWidgetId");
```

#### `CabbageUtils.getChannelId(props, index)`
Returns the ID string of the nth channel from the `channels` array. Throws an error if the channel or its ID is not set.

```javascript
const firstChannelId  = CabbageUtils.getChannelId(this.props, 0);
const secondChannelId = CabbageUtils.getChannelId(this.props, 1);
```

---
title: Custom User Interfaces
description: Custom UI's
---

Cabbage 3 includes a variety of standard plugin controls such as sliders and buttons. However, it also provides straightforward options for creating your own custom elements. There are two primary methods for building custom UIs:

1. ## **Custom Widget Classes**

Create a new widget class and add it to Cabbage. This approach allows you to develop custom widgets while retaining the convenience of the editing tools available in the Cabbage VS Code extension. To achieve this, use the command palette to Create New Custom Widget. If you haven’t already created a custom widget folder, you’ll need to do so first. When this folder is created, the extension will copy the required files into it.

All custom widget classes should be placed in this folder’s widgets sub-folder, i.e, `CustomWidgetFolder/cabbage/widgets`, so the extension can locate them and load them via the property panel. The name of the file you create will also serve as the class name.

By convention, Cabbage classes follow UpperCamelCase, while widget types use lowerCamelCase. Although the backend works with normalised values, frontends send and receive unnormalised values. The backend will use the widget's channels range object to correctly map the unnormalised values to normalised values.

For your widget to be recognized by the Cabbage VS Code extension—especially by the property panel—you must: 

* Add a **`this.props`**:
    This JSON object contains properties accessible through the UI element inspectors in VS Code. Any property defined here can also be queried and modified using the Cabbage get and set opcodes in Csound. Properties can be objects, strings, or numbers. Boolean can be used only for set Cabbage properties such as `visible`, `active`, `automatable`, etc. Use 0/1 if you need to send boolean values to the backend. 

    At a minimum, the props object must include:
    * An 'id' property
    * A channels array
    * An automatable property (boolean)
    * A bounds object to define dimensions and placement
    * A vscode property (assigned to the VS Code API instance when running from VS Code, undefined otherwise)
    * A `zIndex` property (integer)
    * A `visible` property (boolean)
    * An `active` property (boolean)

* Add event listener methods:

    * **`addVsCodeEventListeners(widgetDiv, vs)`**: Called when Cabbage is running from VS Code. Initialise your vscode API instance here.
    * **`addEventListeners()`**: Called when Cabbage is running as a plugin.

Both methods need to be implemented to ensure compatibility with different environments. The simplest pattern is to put all the event handler code into the `addEventListener()` method, and then call it from the `addVsCodeEventListeners()` method. 

* Define a **`getInnerHTML()`** method. This method should return the inner HTML used to render the UI element. The element's size is determined by its bounds object. You can return an svg element or another div element, depending on your design needs. The `WidgetManager` class calls this method when the widget is first inserted (via `insertWidget()`) and whenever properties change (via `updateWidget()`). For canvas-based widgets, `getInnerHTML()` is called during insertion to create the initial DOM structure, but subsequent updates use `updateCanvas()`(see below) instead to avoid destroying the canvas context.

* If you need a canvas for drawing to, add a **`createCanvas()`** function that initialises the canvas, and a **`updateCanvas()`** function that will update the canvas contents. These two functions are called by the `WidgetManager` class to manage the embedded graphics context, and update it when needs be. 

* **Reactive Properties (Optional)**: If you need to listen for changes to widget properties, you can wrap `this.props` with **`CabbageUtils.createReactiveProps()`**. This creates a Proxy that automatically handles common widget behaviors (like toggling pointer-events when `visible` or `active` change) and can notify you of property changes. Call it in your constructor:

```javascript
this.props = CabbageUtils.createReactiveProps(this, this.props, {
    onPropertyChange: (change) => {
        // Called when watched properties change
        // change.key - the property name
        // change.value - new value
        // change.oldValue - previous value
        // change.path - dot-separated path to the property
    },
    watchKeys: null,        // null = watch all, or array of strings/RegExp (e.g., ['value', 'bounds*'])
    mode: 'change',         // 'change' (default) = only notify when value differs, 'set' = notify on every set
    lazyPath: true          // true (default) = compute path only when notifying (more efficient)
});
```

The `opts` parameter is optional - you can call `CabbageUtils.createReactiveProps(this, this.props)` without options for basic reactive behavior. 


> **Performance Note**: Don't use `onPropertyChange` to listen for `value` updates from Csound resulting from calls to `cabbageSetValue`. The `WidgetManager` automatically calls `updateCanvas()` for canvas-based widgets when channel values change, bypassing the reactive props system for efficiency. Value updates are sent as lightweight messages without full widget JSON, allowing high-frequency updates (e.g., for k-rate parameter changes) without overhead. Use reactive props for UI-driven property changes (like `visible`, `bounds`, or custom properties), not for high frequency value streams.

### Sending Data to the Backend

To send data from your widget to the Cabbage backend, use `Cabbage.sendChannelUpdate()`:

```javascript
Cabbage.sendChannelUpdate({
    channel: "myChannel",
    value: 42,
    paramIdx: this.props.channels[0].parameterIndex  // Optional: for automatable parameters
}, this.vscode, this.props.automatable);
```

**Parameters:**
- `message`: Object containing `channel` (string) and `value` (number or string)
- `vscode`: The VS Code API instance (use `this.vscode` in your widget). This is undefined, and safely ignored when running as a plugin.
- `automatable`: Boolean indicating if this is an automatable parameter

**Behavior:**
- If `automatable` is `true`: Routes to `sendParameterUpdate()` for real-time parameter control and DAW automation
- If `automatable` is `false`: Routes to `sendChannelData()` for simple string/numeric data transmission to Csound

You can also call `Cabbage.sendChannelData(channel, data, vscode)` directly for non-automatable data:

```javascript
Cabbage.sendChannelData("myStringChannel", "hello", this.vscode);
Cabbage.sendChannelData("myNumberChannel", 3.14, this.vscode);
```


### Channel Communication

Communication between the back end and front end takes place over named channels. The top-level `this.props.id` represents the main DOM identifier, and most UI updates occur through this channel.

The `channels` array defines the channels used to send value updates from the front end to the back end. If no `this.props.id` is defined, the first `channel.id` in the `channels` array will be used as the primary DOM identifier. 

For multi-channel widgets (like an EQ controller with separate frequency and gain channels for each band), the `WidgetManager` automatically routes incoming parameter updates to the correct channel based on the channel ID. Each channel in the array should have:
- `id`: Unique channel identifier
- `range`: Object with `min`, `max`, `defaultValue`, and optionally `value`
- `parameterIndex`: Optional index for DAW automation (if `automatable` is true) 

### CabbageUtils Helper Functions

The `CabbageUtils` class provides several helper functions for working with widgets:

**`CabbageUtils.getWidgetDivId(props)`**
- Returns the DOM ID for the widget's div element
- Prioritizes `props.id`, then falls back to `channels[0].id`
- Use this for DOM queries like `document.getElementById()`

```javascript
const divId = CabbageUtils.getWidgetDivId(this.props);
```

**`CabbageUtils.getWidgetDiv(channelOrProps)`**
- Returns the actual DOM element for the widget div
- Accepts either a props object or a string div ID
- Returns `null` if element not found

```javascript
const widgetDiv = CabbageUtils.getWidgetDiv(this.props);
// or
const widgetDiv = CabbageUtils.getWidgetDiv("myWidgetId");
```

**`CabbageUtils.getChannelId(props, index)`**
- Returns the ID string of the nth channel from the `channels` array
- Used for accessing specific channels in multi-channel widgets
- Throws an error if the channel or its ID is not set

```javascript
const firstChannelId = CabbageUtils.getChannelId(this.props, 0);
const secondChannelId = CabbageUtils.getChannelId(this.props, 1);
```





2. ## **Entirely new web-based interfaces**

It's also possible to design a completely custom web-based interface using any framework you like. To enable communication with the Csound/Cabbage plugin, you simply need to include the cabbage.js file, which provides the core functions required to send data from the web UI into Csound. While this approach does not provide access to Cabbage’s built-in UI editing tools, it offers maximum flexibility for building interfaces tailored to your needs.

If you want to create an entirely new frontend, with Svelte, React or even vanilla JS, can use the Command Palette to generate a new plugin project. This will create a basic project layout with an HTML file, a CSS file, and a JavaScript file. From there, you can use the Cabbage JS API to communicate with Csound and build your interface however you wish.

To communicate with Csound, you will need to implement event handlers for sending and receiving data. The following example demonstrates a complete setup that communicates to two parameters, with `id`s `slider1` and `slider2`:

```html
<script type="module">
    /* Cabbage JS API integration */
    import { Cabbage } from './cabbage/cabbage.js';
    /* Notify Cabbage that the UI is ready to load */
    Cabbage.sendCustomCommand('cabbageIsReadyToLoad', null);

    // Make handleValueChange available globally
    window.handleValueChange = (newValue, sliderId) => {
        console.log(`Slider ${sliderId} changed to:`, newValue);
        const msg = {
            paramIdx: sliderId === 'slider1' ? 0 : 1,
            channel: sliderId,
            value: parseFloat(newValue),
        };
        const automatable = 1;
        Cabbage.sendChannelUpdate(msg, null, automatable);
    };

    const handleMessage = async (event) => {
        console.log("Message received:", event.data);
        let obj = event.data;

        let slider;
        if (obj.command === "parameterChange") {
            // For parameterChange messages, find slider by paramIdx
            slider = obj.paramIdx === 0 ? document.getElementById('slider1') : document.getElementById('slider2');
        } else {
            // For other messages, find slider by id
            slider = document.getElementById(obj.id);
        }

        if (slider) {
            switch (obj.command) {
                case "parameterChange":
                    console.log(`Parameter change for ${obj.paramIdx}:`, obj);
                    slider.value = obj.value;
                    break;
                case "widgetUpdate":
                    if (obj.value !== undefined) {
                        console.log(`Updating ${obj.id} to value:`, obj.value);
                        slider.value = obj.value;
                    }
                    else if (obj.widgetJson !== undefined) {
                        let widgetObj = JSON.parse(obj.widgetJson);
                        let bounds = widgetObj.bounds;
                        if (bounds) {
                            slider.style.position = 'absolute';
                            slider.style.top = bounds.top + 'px';
                        }
                        // Set value if the UI has just been reopened
                        if (widgetObj.value !== undefined) {
                            slider.value = widgetObj.value;
                        }
                    }
                    break;
                default:
                    break;
            }
        }
    };

    // Add event listener
    window.addEventListener("message", handleMessage);
</script>
```

The script starts by sending a `cabbageIsReadyToLoad` message. This is essential because it informs Cabbage that the web interface is fully loaded and ready to start exchanging data. Without this step, the plugin might miss updates or fail to synchronise with the custom UI.

User interactions, like moving a slider or changing a control, are captured by the global function `handleValueChange`. This function packages the new value and the associated channel information into a message that Cabbage can understand. The script uses `Cabbage.sendChannelUpdate(message, vscode, automatable)` to transmit this data to the audio engine in real time. If `automatable` is set to 1, then this function will also update the host. If set to 0, the data will bypass the host and go straight to Csound. The `vscode` parameter will be null when working outside the larger Cabbage framework, as no VSCode Webview API will be available.

The script also sets up a `handleMessage` listener to capture messages from Csound or the DAW. Messages can be either parameter values sent from the host, or through calls to the `cabbageSetValue/cabbageSet` opcodes. Host parameter change messages are formatted like this:

```json
{
    "command": "parameterChange",
    "paramIdx": number,
    "value": number
}
```

while value updates from Csound, though calls to `cabbageSetValue`, are formatted like this:

```json
{
    "command": "widgetUpdate",
    "id": string,
    "value": value
}
```

Messages can also contain Json data, which can modify widget properties such as visibility or styling. These arrive from calls to the `cabbageSet` opcodes, and are structured like this:

```json
{
    "command": "widgetUpdate",
    "id": string,
    "widgetJson": string
}
```

> You must add dummy parameters to the Cabbage section so that the software can set up the necessary channels and plugin parameters*.
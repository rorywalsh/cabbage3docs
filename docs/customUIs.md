---
title: Custom User Interfaces
description: Custom UI's
---

Cabbage 3 includes a variety of standard plugin controls such as sliders and buttons. However, it also provides straightforward options for creating your own custom elements. There are two primary methods for building custom UIs:

1. ## **Custom Widget Classes**

    Create new widget classes and add them to Cabbage. This approach allows you to develop custom widgets while retaining the convenience of the editing tools available in the Cabbage VS Code extension. To achieve this, follow these steps:

* **Steps to Create a New Widget Class**:

    * **Create a New Widget Class**(): Use an existing widget class as a template. Below are key members you’ll need to define: 
        * **`this.props`**:
            This JSON object contains properties accessible through the UI element inspectors in VS Code. Any property defined here can also be queried and modified using the Cabbage get and set opcodes in Csound. At a minimum, this must include:
            * An 'id' property
            * A channels array
            * An automatable property
            * A bounds object to define dimensions and placement

        * Add Event Listener Methods:
            Implement two methods:

            * **`addVsCodeEventListeners(widgetDiv, vs)`**: Called when Cabbage is running from VS Code.
            * **`addVsCodeEventListeners()`**: Called when Cabbage is running as a plugin.

        Both methods need to be implemented to ensure compatibility with different environments.

        * Define a **`getInnerHTML()`** method. This method should return the inner HTML used to render the UI element. The element’s size is determined by its bounds object. You can return an svg element or another div element, depending on your design needs.

    * Add class to the Cabbage `src/cabbage/widgets` directory. This is installed with the VS Code extension. On MacOS it can be found here in `~/.vscode/extensions`, and on Windows it can be found in `%USERPROFILE%\.vscode\extensions`, where `%USERPROFILE%` is typically `C:\Users\your-username`. When in place, both the VS Code extension and the Cabbage service app will be able to access them. These source files get copied whenever Cabbage export a new plugin.  

2. ## **Entirely new web-based interfaces**

You can design an entirely new web-based interface using any framework you prefer. To ensure communication with the Csound/Cabbage plugin, you need to include the `cabbage.js` file, which provides basic functions to send data to Csound from the web UI. While this method does not give access to the UI editing tools in Cabbage, it offers maximum flexibility to create custom interfaces tailored to your needs.

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

        const slider = document.getElementById(obj.id);
        if (slider) {
            switch (obj.command) {
                case "widgetUpdate":
                    if (obj.value !== undefined) {
                        slider.value = obj.value;
                    }
                    else if (obj.widgetJson !== undefined) {
                        let widgetObj = JSON.parse(obj.widgetJson);
                        let visible = widgetObj.visible;
                        slider.style.display = visible ? 'block' : 'none';
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

User interactions, like moving a slider or changing a control, are captured by the global function `handleValueChange`. This function packages the new value and the associated channel information into a message that Cabbage can understand. The script uses `Cabbage.sendChannelUpdate()` to transmit this data to the audio engine in real time. If 'automatable is set to 1, then this function will also update the host. If set to 0, the data will bypass the host and go straight to Csound. 

The script also sets up a `handleMessage` listener to capture messages from Csound or the DAW. Messages can be either parameter values sent from the host, or through calls to the `cabbageSetValue` opcodes. These messages are structured as follows:

```json
{
    "command": "widgetUpdate",
    "id": "channelId",
    "value": value
}
```

Messages can also contain Json data, which can modify widget properties such as visibility or styling. These arrive from calls to the `cabbageSet` opcodes, and are structured like this:

```json
{
    "command": "widgetUpdate",
    "id": "channelId",
    "widgetJson": JSONDataString
}
```

> You must add dummy parameters to the Cabbage section so that the software can set up the necessary channels and plugin parameters*.

# Cabbage Widgets

While it is possible to create custom widgets using any JavaScript/HTML framework, Cabbage also provides a set of built-in widgets. 

## Widget Channels

Each widget has a unique set of properties and associated Csound software channels, defined in JSON format. These channels define parameters and serve as the communication bridge between Cabbage’s graphical interface and the Csound audio engine. Most widget properties can be modified at any time to adjust their appearance or behavior.

Named channels are a central part of the Cabbage architecture: they carry values and parameter updates between the GUI and Csound, forming a software “bus” for data transfer. Every widget must have a channel `id`. Channel `id`s can be set at the widget’s top level, but more often they are defined within channel objects that form part of the `channels` array. The `channels` array allows multiple channels to be associated with a single widget, enabling extended interactions.

`range` objects are defined within channel objects. These are used both to name plugin parameters and to define their ranges. A typical channel definition with an embedded `range` object might look like this:

```json
{
    "type": "rotarySlider",
    "channels": [
        {
            "id": "Gain", 
            "range": {
                "min": 0, "max": 1, "value": 0, "skew": 1, "increment": 0.01
            }
        }
    ]
}
```

`channel.id`, in this case `"Gain"`, will be registered as a plugin parameter in a host DAW, with `0` and `1` defining its minimum and maximum range. The [`cabbageSetValue`](/docs/cabbage_opcodes/cabbageSetValue) and [`cabbageGetValue`](/docs/cabbage_opcodes/cabbageGetValue) opcodes can be used to send values back and forth to these channels.

Certain widgets, such as a `groupBox`, will rarely be set up to function as parameters. In these cases, a top-level `id` can be set. For example:

```json
{
    "type": "groupBox",
    "id": "adsrPanel"
}
```

In such cases, the [`cabbageSet`](/docs/cabbage_opcodes/cabbageSet) and [`cabbageGet`](/docs/cabbage_opcodes/cabbageGet) opcodes can be used to send JSON data back and forth. Widgets can also combine a top-level `id` with channel `id`s. Consider an `image` widget for example, with multiple channels defined:

```json
{
    "type": "image",
    "channels": [
        {
            "id": "mouseX",
            "event": "mouseMoveX",
            "range": {"min": 0, "max": 1000, "defaultValue": 0, "skew": 1, "increment": 0.01}
        },
        {
            "id": "mouseY",
            "event": "mouseMoveX",
            "range": {"min": 0, "max": 1000, "defaultValue": 0, "skew": 1, "increment": 0.01}
        },
        {
            "id": "image1MousePress",
            "event": "mousePressLeft"
        }
    ]
}
```

📃 **Note:** While it is possible to use `cabbageSet` to update a widget's value, it's not advised to do so. When calling cabbageSet, the widget's entire JSON data is passed from the backend to the frontend. When updating a value using `cabbageSetValue` only the value and channel name are sent, this results in much less overhead. 

If no top-level `id` is set, the `channels[0].id` channel can be used, but the resulting code might not be very intuitive, for instance, calling `cabbageSet` to set the color of `mouseX` doesn’t make much sense. In such cases, it helps to define a more appropriately named top-level `id`:

```json
{
    "type": "image",
    "id": "frequencyXyPad",
    "channels": [
        {
            "id": "mouseX",
            "event": "mouseMoveX",
            "range": {"min": 0, "max": 1000, "defaultValue": 0, "skew": 1, "increment": 0.01}
        },
        {
            "id": "mouseY",
            "event": "mouseMoveY",
            "range": {"min": 0, "max": 1000, "defaultValue": 0, "skew": 1, "increment": 0.01}
        },
        {
            "id": "image1MousePress",
            "event": "mousePressLeft"
        }
    ]
}
```

Using well-named top-level `id`s to manage a widget’s visual state offers many benefits, not least when it comes to debugging complex instruments. 

JSON doesn't support comments. If you wish to add comments to your JSON, use a `"//" : "This is a comment....."` property. The extension will highlight this line to make it stands out from the rest of the JSON code. 

⚠️ **Important:** A widget's range is fixed and cannot be changed at run-time. However, there are ways to make it appear as though the range has changed. Please ask on the forum for tips and tricks on making this work.  

## Widget Properties 

Each and every Cabbage widget has a set of properties that define its behavior and appearance. All properties, except for `channels` and `automatable`, can be updated dynamically during run-time. The following properties are common to all widgets:

**Bounds**

```json
"bounds": {"left":0, "top":0, "width":100, "height":100}
```

* Sets the placement and dimensions of the widget within the main form.

**Visible**

```json
"visible": true
```

* Determines whether the component is visible.

**Active**

```json
"active": true
```

* Will disable a widget if set to `false`. Interaction is not supported with widgets that have `active` set to `false`.

**Automatable**

```json
"automatable": true
```

* Defaults to `true`. Determines if a widget is automatable by a host DAW. Automatable widgets show up as plug-in parameters in the host. Non-automatable widgets can still communicate with Csound but are not accessible by the host. Note that hosts do not allow this parameter to change dynamically. If you change this setting, the plugin will need to be reloaded.

**Z-Index**

```json
"zIndex": 1
```

* Sets the stacking order of the widget. Widgets with higher `zIndex` values appear in front of widgets with lower values. The default is `1`.

Each widget also has a unique set of styling properties accessed through the `style` object. Here, users can control how their widgets look. In a break from Cabbage 2 convention, and to align with CSS/HTML naming schemes, all style properties use CSS-style spelling—for example, background color is listed as `backgroundColor`. A full list of supported styles, along with all other properties, can be found in each widget's manual entry.



## Plugin Parameters and Automation

All widgets include an `automatable` property. Only widgets with `automatable` set to `true` will appear as automatable parameters in a host environment. Through the named channels, these widgets can be controlled or modulated by the host, ensuring synchronisation between the interface and the audio engine. Many of the stock widgets that ship with Cabbage have their `automatable` property set to `true` by default.

Widgets with `automatable:true` can still send and receive data over named channels, but they will not appear in the list of plugin parameters presented in the DAW. A `fileButton` is a good example of one such widget. It makes little sense to give the DAW control to open a native file browser dialog. Note that this property cannot be toggled on and off; the host needs to know what is automatable when it loads.



## Examples and Documentation

Each widget in Cabbage is documented with its properties and available channels. Example .csd files are provided to demonstrate how to integrate the widget into a project and use its channels in practice.


- [Button](button.mdx)
- [Checkbox](checkbox.mdx)
- [ComboBox](combobox.mdx)
- [Form](form.mdx)
- [GenTable](gentable.mdx)
- [GroupBox](groupbox.mdx)
- [Horizontal Slider](horizontalSlider.mdx)
- [Image](image.mdx)
- [Keyboard](keyboard.mdx)
- [Label](label.mdx)
- [Number Slider](numberSlider.mdx)
- [Option Button](optionButton.mdx)
- [Rotary Slider](rotarySlider.mdx)
- [Vertical Slider](verticalSlider.mdx)
- [XY Pad](xyPad.mdx)


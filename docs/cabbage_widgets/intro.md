
# Cabbage Widgets

Cabbage provides a set of built-in widgets, although it is also possible to create custom widgets using any JavaScript/HTML framework. Widgets can generally be divided into two categories: interactive and non-interactive.

## Widget Properties and Channels

Each widget has a unique set of properties and associated Csound software channels, defined in JSON format. These channels define parameters and serve as the communication bridge between Cabbage’s graphical interface and the Csound audio engine. Most widget properties can be modified at any time to adjust their appearance or behavior.

Named channels are a central part of the Cabbage architecture: they carry values and parameter updates between the GUI and Csound, forming a software “bus” for data transfer. Every widget must have a channel `id`. Channel `id`s can be set at the widget’s top level, but more often they are defined within channel objects that form part of the `channels` array. The `channels` array allows multiple channels to be associated with a single widget, enabling extended interactions.

`range` objects can be defined within channel objects. These are used both to name plugin parameters and to define their ranges. A typical channel definition with an embedded `range` object might look like this:

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

`channel.id` — in this case `"Gain"` — will be registered as a plugin parameter in a host DAW, with `0` and `1` defining its minimum and maximum range. The `cabbageSetValue` and `cabbageGetValue` opcodes can be used to send values back and forth to these channels.

Certain widgets, such as a `groupBox`, will rarely be set up to function as parameters. In these cases, a top-level `id` can be set. For example:

```json
{
    "type": "groupBox",
    "id": "adsrPanel"
}
```

In such cases, the `cabbageSet` and `cabbageGet` opcodes can be used to send JSON data back and forth. Widgets can also combine a top-level `id` with channel `id`s. Consider an `image` widget for example, with multiple channels defined:

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

Using well-named top-level `id`s to manage a widget’s visual state offers many benefits, not least when it comes to debugging complex instruments.


## Interactive vs. Non-Interactive Widgets

Interactive widgets (e.g., sliders, buttons, XY pads) can be directly manipulated by the user. When a user changes a value, it is sent through the widget’s named channels to update corresponding Csound parameters.

Non-interactive widgets (e.g., group boxes, images) cannot be directly manipulated by the user. They can only be updated programmatically via Csound.

## Automation

Widgets include an automatable property. Only widgets with automatable set to 1 will appear as automatable parameters in a host environment. Through the named channels, these widgets can be controlled or modulated by the host, ensuring synchronization between the interface and the audio engine.

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


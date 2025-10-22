
# Cabbage Widgets

Cabbage provides a set of built-in widgets, although it is also possible to create custom widgets using any JavaScript/HTML framework. Widgets can generally be divided into two categories: interactive and non-interactive.

## Widget Properties and Channels

Each widget has a unique set of properties and associated Csound software channels, defined in JSON format. These channels define parameters and serve as the communication bridge between Cabbage’s graphical interface and the Csound audio engine. Most widget properties can be modified at any time to adjust appearance or behavior.

Channels are a central part of the Cabbage architecture: they carry values and parameter updates between the GUI and Csound, forming a software “bus” for data transfer. This system allows multiple channels to be associated with a single widget, enabling complex interactions.

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


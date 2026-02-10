---
title: Working with Media Files
description: Managing media files in Cabbage 3
---

Because Cabbage uses a web frontend, all image files used in a UI are sand-boxed. This means that for security reasons, Cabbage UIs can only access files within its own designated directory structure. The browser-based interface cannot directly access files from arbitrary locations on your computer - they must be properly included in your project's folder. 


### File Organization

It's recommended to organize your media files in a structured way:
- Create a `media` folder in your project directory, i.e., the folder that contains your `.csd` file. 
- Place all image files here

### Accessing Media Files

Media files can be selected from the property panel or added manually to a widget's JSON structure:
- Use only the filename and extension. Cabbage will automatically search the media folder from the root directory.
- When using the UI editor, widgets that support image files (e.g., image, rotarySlider) will automatically display a list of available images from the media folder in the File property of the property panel.

📃 **Note:** Most widgets that support images also allow embedding SVG strings, eliminating the need for separate image files. For example:

```json
    "svg"       : {
        "markup": "<svg width=\"39\" height=\"28\" viewBox=\"0 0 39 28\" fill=\"none\" xmlns=\"http://www.w3.org/2000/svg\"> <path d=\"M27.0766 19.6261L37.4187\" fill=\"white\"/> </svg>",
        "padding": {"left": 3, "right": 6, "top": 6, "bottom": 6}
    },
```

### Accessing audio files

Audio files are read by Csound, hence they don't need and special considerations. However, you should also make sure to use full absolute paths for all sound files. The simplest way of doing this is to make sure your sound files are located in the same directory as your .csd file. Then use the `CSD_PATH` reserved channel to construct the full paths:

```
    SFileName1 = "loop1.wav"
    SFileName1 = sprintf("%s/%s", chnget:S("CSD_PATH"), SFileName)
```



<!-- #### Quick access to audio input

Testing arbitrary input signals when working in standalone mode can be cumbersome. The simplest approach is to set up a live microphone input, but this may not always be feasible. If you prefer to route audio files to your standalone plugin, you can do so easily. Right-click the audio file in the VS Code file explorer panel and select the desired channel routing. Once routed, the audio file can be accessed in your code just like any live input, using the inch opcode.

The channel routing will persist across compiles unless manually disabled in the settings. If you'd like to remove all file routing at any time, simply re-select an audio input device. -->

### Bundling Media Files 

When exporting your instrument as a plugin you can use the `package` object from the `form` widget to ensure all files are correctly copied over to the plugin resource direcyory. For example, the following `form` widget will copy all sample from samples from `"/Users/me/cabbage3-recipes/samples/*.wav"` to a folder called `audioSamples` in the exported plugin's resource directory.

```json
{
    "type": "form",
    "caption": "Button Example",
    "size": {"width": 380, "height": 300},
    "guiMode": "queue",
    "pluginId": "def1"
    "package" : {
        "include": [ {"src": "/Users/me/cabbage3-recipes/samples/*.wav", "dest": "audioSamples"} ]
    }
},
```

For more information, see the [`form`](../cabbage_widgets/form.mdx) widget.

📃 **Note:** Images can be included as base64 strings
---
title: Working with Media Files
description: Managing media files in Cabbage 3
---

Because Cabbage uses a web frontend, all media files used in a UI are sand-boxed. This means that for security reasons, Cabbage UIs can only access files within its own designated directory structure. The browser-based interface cannot directly access files from arbitrary locations on your computer - they must be properly included in your project's folder. 


### File Organization

It's recommended to organize your media files in a structured way:
- Create a `media` folder in your project directory, that is the same folder that contains the `.csd` file. 

### Accessing Media Files

When referencing media files in your Cabbage JSON:
- Use only the filename and extension. Cabbage will automatically search the media folder

### Accessing audio files

Audio files are read by Csound, hence they don't need and special considerations. However, you should also make sure to use full absolute paths for all sound files. The simplest way of doing this is to make sure your sound files are located in the same directory as your .csd file. Then use the `CSD_PATH` reserved channel to construct the full paths:

```
    SFileName1 = "loop1.wav"
    SFileName1 sprintf "%s/%s", chnget:S("CSD_PATH"), SFileName
```

<!-- #### Quick access to audio input

Testing arbitrary input signals when working in standalone mode can be cumbersome. The simplest approach is to set up a live microphone input, but this may not always be feasible. If you prefer to route audio files to your standalone plugin, you can do so easily. Right-click the audio file in the VS Code file explorer panel and select the desired channel routing. Once routed, the audio file can be accessed in your code just like any live input, using the inch opcode.

The channel routing will persist across compiles unless manually disabled in the settings. If you'd like to remove all file routing at any time, simply re-select an audio input device. -->

### Bundling Media Files (todo)

When exporting your instrument as a plugin:
- All referenced media files are automatically included in the export
- Files are bundled in the plugin's resource directory
- Maintain the same relative path structure in your code

> Note: Keep your media files optimised for size to ensure efficient plugin loading and distribution. 
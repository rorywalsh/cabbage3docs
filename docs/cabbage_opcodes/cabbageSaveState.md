# cabbageSaveState

This opcode saves the current state of all widget values to a JSON file. The saved state can later be restored using the `cabbageLoadState` opcode. This is useful for creating preset systems or saving/loading configurations. This opcode works at i-time only. Therefore it is best used in an instrument that is called when you want to save state. 

## Syntax
```csound
cabbageSaveState:i(SFilePath)
cabbageSaveState:i(SFilePath, SWidgetIds[])
```

### Initialization
* *SFilePath* – the absolute file path where the state will be saved (e.g., "/Users/username/Documents/mypreset.json" or "C:\\Users\\username\\Documents\\mypreset.json"). The file will be created if it doesn't exist, or overwritten if it does. Relative paths are not supported.
* *SWidgetIds[]* – (optional) a string array of widget IDs that should be saved with their full JSON (all properties). All other widgets are still saved, but with channel data only (id and channel values). If omitted, all widgets are saved with channel data only.

> Note: The saved JSON file contains all current widget channel values and can be edited manually if needed. To save multiple presets, use Csound's string formatting to dynamically generate unique filenames, for example: `sprintf("/path/to/presets/preset_%d.json", iPresetNumber)`

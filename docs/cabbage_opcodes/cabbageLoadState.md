# CabbageLoadState

This opcode loads widget values from a previously saved JSON state file created by the `cabbageSaveState` opcode. All matching widget channels will be updated with their saved values. Unlike Cabbage 2, all widget state is saved and restored, not only the current parameter values. 

## Syntax

**cabbageLoadState** *SFilePath*

### Initialization
* *SFilePath* – the absolute file path to the state file to load (e.g., "/Users/username/Documents/mypreset.json" or "C:\\Users\\username\\Documents\\mypreset.json"). The file must exist and contain valid JSON data. Relative paths are not supported.

> Note: Only widgets with channels that match those in the saved state file will be updated. Widgets not present in the state file will retain their current values. To load different presets, use Csound's string formatting to dynamically generate filenames, for example: `sprintf("/path/to/presets/preset_%d.json", iPresetNumber)`

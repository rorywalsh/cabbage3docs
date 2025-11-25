---
title: Exporting Instruments
description: How to export instruments
---

Once you are satisfied that your plugin is ready for testing in a DAW, you can export it using the `Export as...` command. A list of plugin export options, specific to your current operating system, will be displayed. After selecting an export option, a file browser window will appear, allowing you to choose the target destination for your plugin binary.

The plugin binary will be saved in the selected location. By default, any resources the plugin requires—such as images, .csd files, and samples—will be automatically written to the following locations unless Bundle Resources is enabled:

* MacOS
    `/Library/CabbageAudio/PLUGIN_NAME/`
* Windows
    `C:/ProgramData/CabbageAudio/PLUGIN_NAME/`
 
`PLUGIN_NAME` in the folder path will match the name of your exported plugin. It is crucial that the folder name exactly matches the plugin binary name. Cabbage ensures this alignment during the export process, so avoid renaming these folders, as doing so may result in unexpected behavior within Cabbage.

To make changes to your newly exported plugin, you only need to edit the associated .csd file; there’s no need to re-export the plugin each time you makes changes. For example, on Windows, if your plugin is named `SavageCabbage.dll`, you can make changes by editing the corresponding file located at:
`C:/Program Files/CabbageAudio/SavageCabbage/SavageCabbage.csd`.

After making changes, you must remove and re-add the plugin in your plugin host (DAW) to see the updates. Once the plugin is removed and reinstated on the track, the changes will be reflected. The simplest approach here is to simply reload your plugin project in your DAW. In almost all cases this is quicker than removing the track and re-adding it. However, if you have add new parameters to your plugin, you may have problems opening a saved session as the DAW will expect a certain number of parameters. In this case you will need to start a new session to test. 

### Bundling Resources
If you enable the Bundle Resource option in the Cabbage VS Code settings, Cabbage will place the Resource folder inside the plugin bundle. This is useful when distributing a plugin but can cause code signing issues on macOS during development. Each time you modify a file within the plugin bundle, you must re-sign the plugin.

To avoid this, it's recommended to keep your resources in the directories mentioned above during development. This allows for easier file updates without the need for repeated code signing.

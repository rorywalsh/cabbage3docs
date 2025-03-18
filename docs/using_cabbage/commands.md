---
title: Cabbage Commands
description: Available commands in Cabbage 3
---

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Command Palette Access](#command-palette-access)
- [Commands](#commands)
  - [Running](#running)
  - [Formatting](#formatting)
  - [Utilities](#utilities)
  - [Configuration](#configuration)
  - [Exporting](#exporting)

## Command Palette Access
Ctrl+S and Ctrl+E are the default shortcuts for running and entering edit mode. The following commands, which don't have keyboard shortcuts attached, are all accessible from the command palette. To access the command palette in Visual Studio Code, you can use the following keyboard shortcuts:

- **Windows/Linux**: Press `Ctrl + Shift + P`
- **macOS**: Press `Cmd + Shift + P`

Once the command palette is open, you can start typing the name of the command you want to execute. For example, you can type "Cabbage" to filter the commands related to the Cabbage extension. Select the desired command from the list to execute it. Below are the commands currently provided. 

> It's very simple to assign custom shortcuts to any command palette entry. Simple summon the command, then press the small cogwheel icon that appears on the right of the command. This will bring up a config screen where you can quickly set your preferred shortcuts.  

## Commands

### Running

- **Launch Cabbage**
  - The `Compile Instrument` command can be called from the command palette. Each time it is called your .csd file will be saved to disk, and if it contains a valid Cabbage JSON section the instrument will launch is a dedicated tab.

- **Edit Mode**
  - `Edit Mode` enabled edit mode for the Cabbage interface. When in edit mode users can right-click to show the context menu, whereupon they can select a widget to add to the UI. Clicking on an existing widget will being up its properties panel.

### Formatting

- **Format Document**
  - Formats the current document according to Cabbage formatting rules (this basically).

- **Collapse Cabbage section**
  - Collapses the Cabbage JSON section in the current document.

- **Expand Cabbage section**
  - Expands the Cabbage JSON section in the current document.

### Utilities

- **Jump to Widget Object**
  - Provides a dropdown menu of widget objects. Selecting one will cause the text editor to jump that that object. Objects are listed by their channel name. 

- **Open a widget example**
  - Provides a dropdown list of example widget .csd files. Selecting one will open it in text editor. Any of these files can be run without modification, but they are read-only. If you wish to modify an example you will need to run 'save-as' to make an editable copy. 
  

### Configuration

- **Select Sampling Rate**
  - Opens a prompt to select the audio sampling rate for the project.

- **Select Buffer Size**
  - Opens a prompt to select the audio buffer size for the project.

- **Select Audio Driver**
  - Opens a prompt to select the audio driver.
  
- **Select Audio Output Device**
  - Opens a prompt to select the audio output device.

- **Select Audio Input Device**
  - Opens a prompt to select the audio input device.

- **Select MIDI Input Device**
  - Opens a prompt to select the MIDI input device.

- **Select MIDI Output Device**
  - Opens a prompt to select the MIDI output device.

- **Set Cabbage source path**
  - Opens a dialog to set the path to the Cabbage JS source directory. 
  > This is set by the extension and should not be overwritten unless you know what you are doing!

- **Set path to the Cabbage binary**
  - Opens a dialog to set the path to the Cabbage binary executable, that is CabbageApp.app on MacOS and CabbageApp.exe on Windows. 
  > This is also set by the extension and should not be overwritten unless you know what you are doing!

### Exporting

- **Export as VST3 Effect**
  - Opens a file dialogue and lets users export the current project as a VST3 effect plugin. 

- **Export as VST3 Synth**
  - Opens a file dialogue and lets users export the current project as a VST3 synthesizer plugin.

- **Export as AUv2 Effect**
  - Opens a file dialogue and lets users export the current project as an AUv2 effect plugin.

- **Export as AUv2 Synth**
  - Opens a file dialogue and lets users export the current project as an AUv2 synthesizer plugin.

- **Bundle Resources**
  - Tells Cabbage to bundle all resources into the plugin folder, otherwise all resources, including the .csd file will be placed into the CabbageAdio resources directory.  

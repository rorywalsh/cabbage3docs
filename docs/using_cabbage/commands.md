---
title: Commands & Settings
description: Available commands and settings in Cabbage 3
---

## Table of Contents
- [Command Palette Access](#command-palette-access)
- [Commands \& Settings](#commands--settings)
  - [Running \& Compilation](#running--compilation)
  - [Document Formatting](#document-formatting)
  - [Navigation](#navigation)
  - [Project Creation](#project-creation)
  - [Audio/MIDI Configuration](#audiomidi-configuration)
  - [Audio Recording](#audio-recording)
  - [Plugin Export](#plugin-export)
  - [Pro Plugin Export](#pro-plugin-export)
  - [Custom Widgets](#custom-widgets)
  - [Daisy Development](#daisy-development)
  - [Advanced Settings](#advanced-settings)
  - [Utilities](#utilities)

## Command Palette Access

**Ctrl+S** and **Ctrl+E** are the default shortcuts for compiling and entering edit mode. All other commands are accessible from the command palette:

- **Windows/Linux**: Press `Ctrl + Shift + P`
- **macOS**: Press `Cmd + Shift + P`

Once open, type "Cabbage" to filter extension commands.

> **Tip**: Assign custom shortcuts to any command by clicking the cogwheel icon next to the command in the palette.

## Commands & Settings

### Running & Compilation

**Commands:**

- **Compile Cabbage Instrument** (`cabbage.compile`)
  - Saves the current .csd file and launches the instrument in a dedicated webview tab if it contains valid Cabbage JSON

- **Start Cabbage Server** (`cabbage.startServer`)
  - Manually starts the Cabbage backend server (can also be started from the bottom right of the status panel)

- **Stop Cabbage Server** (`cabbage.stopServer`)
  - Stops the running Cabbage backend server

- **Edit Mode** (`cabbage.editMode`)
  - Toggles edit mode for the Cabbage interface. Right-click in edit-mode to add widgets or click existing widgets to edit their properties

- **Stop Csound** (`cabbage.stopCsound`)
  - Stops the running Csound process

**Settings:**

- **Clear Console On Compile** (`cabbage.clearConsoleOnCompile`)
  - Default: `true`
  - Clear the console output each time Csound is compiled

- **Log Verbose** (`cabbage.logVerbose`)
  - Default: `false`
  - Enable verbose logging from Cabbage for troubleshooting

### Document Formatting

**Commands:**

- **Format Document** (`cabbage.formatDocument`)
  - Formats the current .csd document according to Cabbage formatting rules and JSON settings

- **Expand Cabbage section** (`cabbage.expandCabbageJSON`)
  - Expands the `<Cabbage>` JSON section for easier editing

- **Collapse Cabbage section** (`cabbage.collapseCabbageJSON`)
  - Collapses the `<Cabbage>` JSON section to reduce visual clutter

- **Add a Cabbage section** (`cabbage.addCabbageSection`)
  - Inserts a new `<Cabbage>` section into the current document

- **Move Cabbage Section** (`cabbage.moveCabbageSection`)
  - Moves the existing `<Cabbage>` section to the top or bottom of the .csd file

**Settings:**

- **Default JSON Formatting** (`cabbage.defaultJsonFormatting`)
  - Default: `"Single line objects"`
  - Options: `"Single line objects"` | `"Multiline objects"`
  - Choose how widget objects are formatted in the `<Cabbage>` section

- **JSON Indent Spaces** (`cabbage.jsonIndentSpaces`)
  - Default: `4`
  - Range: 2-8
  - Number of spaces to use for JSON indentation

- **JSON Max Length** (`cabbage.jsonMaxLength`)
  - Default: `120`
  - Range: 0-200
  - Maximum line length for JSON formatting. Longer lines will be wrapped. Set to 0 for no wrapping

- **Show Warning Comment** (`cabbage.showWarningComment`)
  - Default: `true`
  - Show a warning comment above the `<Cabbage>` section when the extension writes JSON into the document

- **Snap To Size** (`cabbage.snapToSize`)
  - Default: `4`
  - Number of pixels to move by when dragging widgets in edit mode

### Navigation

**Commands:**

- **Jump to widget definition** (`cabbage.jumpToWidgetObject`)
  - Shows a dropdown of all widgets in the current file. Select one to jump to its JSON definition

- **Go to widget definition** (`cabbage.goToDefinition`)
  - Context menu command to jump to a widget's definition from a reference in the code

- **Reorder Widgets** (`cabbage.reorderWidgets`)
  - Reorders widgets in the `<Cabbage>` section based on their position in the UI

### Project Creation

**Commands:**

- **Create a new Cabbage Effect file** (`cabbage.createNewCabbageEffect`)
  - Creates a new .csd file with a basic effect template

- **Create a new Cabbage Synth file** (`cabbage.createNewCabbageSynth`)
  - Creates a new .csd file with a basic synthesizer template

- **Create Vanilla VST3 Effect** (`cabbage.createVanillaVST3Effect`)
  - Creates a new project with custom HTML/CSS/JS frontend for a VST3 effect

- **Create Vanilla VST3 Synth** (`cabbage.createVanillaVST3Synth`)
  - Creates a new project with custom HTML/CSS/JS frontend for a VST3 synth

### Audio/MIDI Configuration

**Commands:**

- **Select Sampling Rate** (`cabbage.selectSamplingRate`)
  - Choose the audio sampling rate (e.g., 44100, 48000, 96000 Hz)

- **Select Buffer Size** (`cabbage.selectBufferSize`)
  - Choose the audio buffer size (affects latency vs. CPU usage)

- **Select Audio Driver** (`cabbage.selectAudioDriver`)
  - Choose the audio driver (Windows only: ASIO, DirectSound, etc.)

- **Select Audio Output Device** (`cabbage.selectAudioOutputDevice`)
  - Choose which audio output device to use

- **Select Audio Input Device** (`cabbage.selectAudioInputDevice`)
  - Choose which audio input device to use

- **Select MIDI Input Device** (`cabbage.selectMidiInputDevice`)
  - Choose which MIDI input device to use

- **Select MIDI Output Device** (`cabbage.selectMidiOutputDevice`)
  - Choose which MIDI output device to use

- **Send file to stereo inputs** (`cabbage.sendFileToChannel1and2`)
  - Routes an audio file to both input channels 1 and 2

- **Send file to input 1** (`cabbage.sendFileToChannel1`)
  - Routes an audio file to input channel 1

- **Send file to input 2** (`cabbage.sendFileToChannel2`)
  - Routes an audio file to input channel 2

#### Audio Recording

**Commands:**

- **Start Recording to WAV** (`cabbage.startRecording`)
  - Opens a file browser to select output location and starts recording the processed audio output to a WAV file
  - Records in real-time while your instrument is performing
  - Shows a live status bar indicator with elapsed time (e.g., `🔴 Recording: recording.wav [00:23]`)
  - Click the status bar to stop recording, or use the Stop Recording command

- **Stop Recording** (`cabbage.stopRecording`)
  - Stops the current recording and saves the WAV file
  - Recording also stops automatically when:
    - You close the instrument panel
    - You use "Stop Csound" command
    - You enter Edit Mode

> **Note**: Recording captures the final processed audio output (post-Csound processing) at the current audio system sample rate.

**Recording Settings:**

- **Recording Bit Depth** (`cabbage.recordingBitDepth`)
  - Default: `"32-bit float"`
  - Options: `"16-bit"` | `"32-bit float"`
  - Bit depth for audio recording
    - **16-bit**: Smaller file size, suitable for most music applications
    - **32-bit float**: Higher dynamic range and precision, no clipping, larger file size

**Settings:**

> These settings are managed by the commands above and stored in VS Code settings. They can also be edited directly in settings.json. Updating them via the command pallete will also display a list of valid options.

- **Audio Output Device** (`cabbage.audioOutputDevice`)
  - Default: `"Default"`
  - Currently selected audio output device

- **Audio Input Device** (`cabbage.audioInputDevice`)
  - Default: `"Default"`
  - Currently selected audio input device

- **MIDI Output Device** (`cabbage.midiOutputDevice`)
  - Default: `"Default"`
  - Currently selected MIDI output device

- **MIDI Input Device** (`cabbage.midiInputDevice`)
  - Default: `"Default"`
  - Currently selected MIDI input device

- **Audio Sample Rate** (`cabbage.audioSampleRate`)
  - Default: `"44100"`
  - Currently selected sampling rate

- **Audio Buffer Size** (`cabbage.audioBufferSize`)
  - Default: `"32 samples"`
  - Currently selected buffer size

- **Audio Driver** (`cabbage.audioDriver`)
  - Default: `"32 samples"`
  - Currently selected audio driver (Windows only)

### Plugin Export

**Commands:**

- **Export as VST3 Effect** (`cabbage.exportVST3Effect`)
  - Exports the current instrument as a VST3 effect plugin

- **Export as VST3 Synth** (`cabbage.exportVST3Synth`)
  - Exports the current instrument as a VST3 synthesizer plugin

- **Export as AUv2 Effect** (`cabbage.exportAUEffect`)
  - Exports the current instrument as an AUv2 effect plugin (macOS only)

- **Export as AUv2 Synth** (`cabbage.exportAUSynth`)
  - Exports the current instrument as an AUv2 synthesizer plugin (macOS only)

- **Export as CLAP Effect** (`cabbage.exportCLAPEffect`)
  - Exports the current instrument as a CLAP effect plugin

- **Export as CLAP Synth** (`cabbage.exportCLAPSynth`)
  - Exports the current instrument as a CLAP synthesizer plugin

- **Export as AUv2 MidiFx** (`cabbage.exportAUMidiFx`)
  - Exports the current instrument as an AUv2 MidiFx plugin (macOS only)

#### Pro Plugin Export

📃 **Note:** These commands are only available in the 'pro' build of Cabbage.

- **Setup Pro Binaries** (`cabbage.setupCabbageProBinaries`)
  - Sets up the paths to Cabbage Pro binaries for encrypted plugin export

- **Export as VST3 Effect (Pro)** (`cabbage.exportProVST3Effect`)
  - Exports the current instrument as a VST3 effect plugin with encryption (requires Pro)

- **Export as VST3 Synth (Pro)** (`cabbage.exportProVST3Synth`)
  - Exports the current instrument as a VST3 synthesizer plugin with encryption (requires Pro)

- **Export as CLAP Effect (Pro)** (`cabbage.exportProCLAPEffect`)
  - Exports the current instrument as a CLAP effect plugin with encryption (requires Pro)

- **Export as CLAP Synth (Pro)** (`cabbage.exportProCLAPSynth`)
  - Exports the current instrument as a CLAP synthesizer plugin with encryption (requires Pro)

- **Export as AUv2 Effect (Pro)** (`cabbage.exportProAUEffect`)
  - Exports the current instrument as an AUv2 effect plugin with encryption (requires Pro, macOS only)

- **Export as AUv2 Synth (Pro)** (`cabbage.exportProAUSynth`)
  - Exports the current instrument as an AUv2 synthesizer plugin with encryption (requires Pro, macOS only)

- **Export as AUv2 MidiFx (Pro)** (`cabbage.exportProAUMidiFx`)
  - Exports the current instrument as an AUv2 MidiFx plugin with encryption (requires Pro, macOS only)

**Settings:**

- **Bundle Resources** (`cabbage.bundleResources`)
  - Default: `false`
  - When enabled, all resources (audio files, images, etc.) are bundled into the plugin directory. When disabled, resources are placed in the CabbageAudio resources folder

- **Property Panel Position** (`cabbage.propertyPanelPosition`)
  - Default: `"right"`
  - Options: `"right"` | `"left"`
  - Position of the property panel in the webview editor

### Custom Widgets

**Commands:**

- **Select Custom Widget Folder** (`cabbage.setCustomWidgetDirectory`)
  - Choose a folder for custom widgets. Automatically copies the required Cabbage framework structure

- **Create New Custom Widget** (`cabbage.createNewCustomWidget`)
  - Creates a new custom widget class from a template in your custom widgets folder

**Settings:**

- **Custom Widget Folders** (`cabbage.customWidgetDirectories`)
  - Default: `[]`
  - Array of paths to custom widget folders. Each folder should contain a `cabbage` folder structure
  - **Recommended**: Use the "Select Custom Widget Folder" command which automatically sets up the required structure

### Daisy Development

Commands for building Csound code for the [Electrosmith Daisy](https://www.electro-smith.com/daisy) hardware platform:

**Commands:**

- **Make for Daisy** (`cabbage.makeForDaisy`)
  - Compiles the current .csd file for Daisy hardware

- **Make clean for Daisy** (`cabbage.makeCleanForDaisy`)
  - Cleans the Daisy build directory

- **Make boot for Daisy** (`cabbage.makeBootForDaisy`)
  - Creates a bootloader for Daisy

- **Make dfu for Daisy** (`cabbage.makeDfuForDaisy`)
  - Creates a DFU (Device Firmware Update) file for Daisy

- **Select Csound Include Folder (for Daisy)** (`cabbage.setCsoundIncludeDir`)
  - Sets the path to Csound header files needed for Daisy compilation

- **Select Csound Library Folder (for Daisy)** (`cabbage.setCsoundLibraryDir`)
  - Sets the path to Csound library files needed for Daisy compilation

**Settings:**

- **Folder Containing Csound Includes** (`cabbage.pathToCsoundIncludeDir`)
  - Default: `""`
  - Folder containing Csound includes - used when building for Daisy

- **Folder Containing Csound Library** (`cabbage.pathToCsoundLibraryDir`)
  - Default: `""`
  - Folder containing Csound library - used when building for Daisy

### Advanced Settings

**Commands:**

- **Select Cabbage Source Folder** (`cabbage.setCabbageSourcePath`)
  - Sets the path to the Cabbage JavaScript source folder
  > ⚠️ **Warning**: This is set automatically by the extension. Only change if you know what you're doing!

- **Select Cabbage Binary Folder** (`cabbage.setCabbageBinaryPath`)
  - Sets the path to the Cabbage backend executable (CabbageApp)
  > ⚠️ **Warning**: This is set automatically by the extension. Only change if you're using a custom build!

- **Reset CabbageApp (not vscode) settings file** (`cabbage.resetCabbageAppSettingsFiles`)
  - Resets the Cabbage backend settings file to defaults (does not affect VS Code settings)

- **Set Custom Comment Decoration Color** (`cabbage.setCustomCommentDecorationColor`)
  - Sets the color for comment decorations in Cabbage JSON sections

**Settings:**

- **Folder Containing Cabbage Service App** (`cabbage.pathToCabbageBinary`)
  - Default: `""`
  - Folder containing Cabbage service app. Leave empty to use the default location bundled with the extension

- **Folder Containing Cabbage Javascript on Windows** (`cabbage.pathToJsSourceWindows`)
  - Default: `""`
  - Folder containing Cabbage Javascript on Windows. Leave empty to use default location

- **Folder Containing Cabbage Javascript on macOS** (`cabbage.pathToJsSourceMacOS`)
  - Default: `""`
  - Folder containing Cabbage Javascript on macOS. Leave empty to use default location

- **Folder Containing Cabbage Javascript on Linux** (`cabbage.pathToJsSourceLinux`)
  - Default: `""`
  - Folder containing Cabbage Javascript on Linux. Leave empty to use default location

### Utilities

**Commands:**

- **Open an widget example** (`cabbage.openCabbageExample`)
  - Browse and open example .csd files demonstrating various widgets and techniques

- **Opens the Csound 7 opcode reference page** (`cabbage.openOpcodeReference`)
  - Opens the Csound 7 opcode documentation in your browser

- **Update old-style Cabbage code to JSON** (`cabbage.updateToCabbage3`)
  - Converts old Cabbage syntax to the new JSON format

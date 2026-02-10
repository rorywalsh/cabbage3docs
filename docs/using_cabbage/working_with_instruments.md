---
title: Working with Instruments
description: How to work with Cabbage instruments
---

Once the Cabbage extension is enabled in Visual Studio Code, you can start developing instruments immediately. Whenever you save a .csd file (Unified Csound Document) that contains a `<Cabbage>` JSON block, the extension automatically loads the instrument’s UI in a live preview panel. This lets you view and interact with the interface in real time, giving immediate feedback on your design.

To access Edit Mode, open the command palette (press Ctrl+Shift+P on Windows/Linux or Cmd+Shift+P on macOS) and select the `vscabbage: Enter Edit Mode` command. In Edit Mode, you can adjust widget properties such as dimensions, colors, fonts, and more to customize your instrument's UI. Each modification updates the instrument's Cabbage JSON code in real-time, enabling quick iteration.

Once you're satisfied with your changes, save the .csd file ( you will need to focus the .csd text). Saving will close the UI editor and return you to Performance Mode, where you can test the instrument as it would appear in a live environment. 

📃 **Note:** All VS Code commands can be assigned keyboard shortcuts to help speed up development. 
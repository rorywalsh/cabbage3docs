---
title: Running Cabbage
description: Running the Cabbage server
---

The Cabbage VS Code extension includes a background service that acts as a server for Cabbage 3 instruments and effects within the IDE. After you install the extension, a Run Cabbage icon appears in the lower‑right corner of the VS Code status bar. Clicking it starts the background service and sets up a communication protocal between Cabbage and VS Code.

Whenever you save a .csd file while the Cabbage server is running, Cabbage parses the contents of the `<Cabbage>` section and sends it to VS Code, which then constructs the UI accordingly. You can start or restart the server as often as needed, and it will automatically restart whenever you change the extension’s settings. When running your instruments as plugins, communication between the frontend and the plugin is handled directly through a serious of callbacks. Although the means in which the back and frontend communicate differs between the VS Code extension, and the plugin interface, the user experience remains the same. 

---
title: Running Cabbage
description: Running the Cabbage server
---

The Cabbage VS Code extension includes a background service that acts as a server for Cabbage 3 instruments and effects within the IDE. After you install the extension, a Run Cabbage icon appears in the lower‑right corner of the VS Code status bar. Clicking it starts the background service and opens a WebSocket connection between Cabbage and VS Code.

Whenever you save a .csd file while the Cabbage server is running, Cabbage parses the contents of the `<Cabbage>` section and sends it to VS Code, which then constructs the UI accordingly. All communication between Cabbage and VS Code travels over this WebSocket connection. You can start or restart the server as often as needed, and it will automatically restart whenever you change the extension’s settings.

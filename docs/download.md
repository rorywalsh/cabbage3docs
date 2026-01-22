---
title: Download and Install
description: Download and Install
---

***Cabbage 3** and the associated Visual Studio Code extension are currently in ***Alpha*** development. These releases are experimental and may undergo significant changes. Features are not final, and stability or performance may vary. Use at your own discretion, and expect frequent updates and potential breaking changes.*


Cabbage 3 uses Csound7 across all platforms.You can find platform installers for the pre-release betas [here](https://github.com/csound/csound/releases).

The beta installers for Windows and macOS are not code-signed. This means you will need to explicitly allow the operating system to bypass its default security restrictions.

**macOS:**
After attempting to run the installer and being blocked, open **System Settings → Privacy & Security**. Scroll to the bottom of the page, where you will see a message indicating that the installer was blocked. Click **“Open Anyway”** to proceed.

**Windows:**
When prompted that the application may be unsafe, click **“More info”**, then select **“Run anyway”** to continue the installation.

> On MacOS you may need to codesign the Csound executable. To do so, run this command from ther terminal: `codesign -s - /Applications/Csound/CsoundLib64.framework --timestamp --force --deep`

The latest Cabbage Visual Studio Code extension can be found from the [`vscabbage`](https://github.com/rorywalsh/vscabbage/releases) releases page. Once you download the relevant .vsix file you will need to manually install it in VS Code. You can manually install a VS Code extension using the `Install from VSIX` command in the Extensions view command dropdown, or the `Extensions: Install from VSIX command` in the Command Palette.

⚠️ **Important:** To take advantage of Csound language features, you should also install the [`csound-vscode-plugin`](https://marketplace.visualstudio.com/items?itemName=kunstmusik.csound-vscode-plugin). This plugin adds syntax highlighting, opcode hints, error-checking and much more. It is available in the Visual Studio Code marketplace and can be installed from the Extensions panel within Visual Studio Code. 


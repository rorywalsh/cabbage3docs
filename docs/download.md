---
title: Download and Install
description: Download and Install
---

***Cabbage 3** and the associated Visual Studio Code extension are currently in ***Alpha*** development. These releases are experimental and may undergo significant changes. Features are not final, and stability or performance may vary. Use at your own discretion, and expect frequent updates and potential breaking changes.*


Cabbage 3 uses Csound7 across all platforms. Here are links to the Windows and MacOS version that Cabbage3 is build with:
* [MacOS](https://www.dropbox.com/scl/fi/d5hnkcecizlwgvnaw1yjy/csound-7.zip?rlkey=pf9v3ucfo8hecyl5ahbacr0a0&dl=1)
* [Windows](https://dl.dropboxusercontent.com/scl/fi/18ppri60nupdrwyo1zt1x/csound-7.exe?rlkey=m6592gt8pfkhvirnl17rbrwfh&st=cml9vetz)

> On MacOS you may need to codesign the Csound executable. To do so, run this command from ther terminal: `codesign -s - /Applications/Csound/CsoundLib64.framework --timestamp --force --deep`

The latest Cabbage Visual Studio Code extension can be found from the [`vscabbage`](https://github.com/rorywalsh/vscabbage/releases) releases page. Once you download the relevant .vsix file you will need to manually install it in VS Code. You can manually install a VS Code extension using the `Install from VSIX` command in the Extensions view command dropdown, or the `Extensions: Install from VSIX command` in the Command Palette.

⚠️ **Important:** To take advantage of Csound language features, you should also install the `csound-vscode-plugin`. This plugin adds syntax highlighting, opcode hints, error-checking and much more. It is available in the Visual Studio Code marketplace and can be installed from the Extensions panel within Visual Studio Code. 


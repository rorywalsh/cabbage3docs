<details>
<summary>
I can't see any interface when I compile an instrument from my .csd file in VS Code?
</summary> 
<p>When the VS Code extension compiles an instrument for the first time, it attempts to create a new <code>settings.json</code> file. This file is read by the Cabbage service application running in the background. It includes a path to several <code>.js</code> files required for parsing the Cabbage section of the <code>.csd</code> file. If this path is empty, the UI will not appear. The easiest fix is to use the 'Reset CabbageApp settings file' command to clear the file. The next time you compile an instrument, the UI should load correctly.</p> 
</details> 


<details> 
<summary>
My plugin loads fine, but my custom UI is unresponsive?
</summary> 
<p>The most common cause of this issue is an error in your JavaScript code. If the plugin's UI is unresponsive, you won't be able to open the developer tools, making debugging more challenging. The simplest solution is to comment out portions of your code incrementally. Start by commenting out widgets in the Cabbage section of your <code>.csd</code> file to identify the widget causing the issue. Once identified, review the corresponding <code>.js</code> file. Comment out larger chunks of code initially. If the UI becomes responsive, albeit without full functionality, start uncommenting sections gradually until you pinpoint the error in your code.</p> 
</details>

<details> 
<summary> 
Something is wrong but I don't know what? 
</summary> 
<p>If something is not working as expected, you should enable the <code>verbose logging</code> setting in the extension settings. This will generate an extension log of messages in the Cabbage output console, which may help diagnose the issue. Additionally, you can launch the developer web tools panel via the command palette. The Cabbage UI in VS Code is a web panel—essentially an embedded web page. The developer console allows you to inspect elements and review the console log for errors. Both of these features should help you identify the problem. Once you’ve pinpointed the issue, you can post the logs and relevant information to the Cabbage user forum for further assistance.</p> 
</details>


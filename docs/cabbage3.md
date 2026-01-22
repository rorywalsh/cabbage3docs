---
title: What's new in v.3
description: Cabbage 3
---

Cabbage 3 represents a significant overhaul of the previous version, Cabbage 2. This transition involved tough decisions that could lead to some discomfort for existing users, as it diverges from familiar practices. Below are some of the notable changes:

#### 1. Transition to a VS-Code Extension
- One of the most impactful changes is the removal of the Cabbage Integrated Development Environment (IDE). In its place, users are encouraged to use a Visual Studio Code (VS-Code) extension. This decision streamlined the project, resulting in a codebase that is nearly 50% smaller. This reduction not only simplifies the development process but also minimizes ongoing maintenance challenges that come with managing a standalone IDE. By leveraging VS-Code, a widely used and robust code editor, Cabbage can now benefit from a rich ecosystem of extensions, community support, and frequent updates.

#### 2. Adoption of WebViews for User Interfaces
- The redesign includes a shift to using WebViews for rendering user interfaces. This transition allows developers to create customized UIs without needing to engage with C++ code directly, thereby eliminating the complexity of recompiling or modifying the Cabbage codebase. Users can now harness the power of established web front-end frameworks like React, Vue, and Svelte, along with their extensive component libraries. This change empowers developers to create modern, responsive, and visually appealing interfaces using familiar web technologies, enhancing the user experience significantly.

#### 3. Change in Syntax
- Perhaps one of the most notable adjustments in Cabbage 3 is the alteration in syntax, specifically the transition from traditional identifiers to the use of JSON objects. In the earlier version, users would typically rely on a system of identifiers to define various components and functionalities within their projects. This might have included unique names and values associated with different elements of the user interface or functionality within the Cabbage environment.

JSON or JavaScript Object Notation, is a lightweight data interchange format that is easy for humans to read and write and easy for machines to parse and generate. By transitioning to JSON objects, Cabbage 3 enhances the expressiveness and flexibility of how data is structured and manipulated. JSON allows for nested structures, making it easier to represent complex data relationships and configurations in a way that is both human-readable and machine-friendly.

- #### Implications for Users
    This change has several implications:
    - **Improved Clarity and Structure**: The use of JSON can lead to clearer, more organized code, as developers can nest objects to represent hierarchies and relationships. This could make understanding and maintaining code easier.
    - **Simplified Data Handling**: JSON's widespread adoption in web development means that many developers will already be familiar with its syntax and structure, potentially lowering the learning curve.
    - **Increased Interoperability**: By using a format that is compatible with various web technologies, Cabbage 3 may offer better integration with other tools and systems that utilize JSON, fostering a more collaborative development environment.

#### 4. Changes in Identifier Naming and Structure in Cabbage 3

Another cause of potential frustration in this move is the fact that **camelCase** is now being used across all properties, including widget names. Additionally, abbreviations have been expanded for clarity. For example `rslider` is now changed to `rotarySlider`, `combbox` to `comboBox`, `filebutton` to `fileButton`, etc.

Also, certain identifier names have been modified. For instance, `outlineWidth` and `outlineColour` are now part of the `stroke` object within the `colour` object:

    ```json
    "colour":{
        "stroke": {
            "width": 2,
            "colour": "yellow"
        }
    }
```

Other identifiers have been dropped completely. Please refer to the updated Docs section to see how widget properties have been changed and updated.

In summary, the changes in Cabbage 3, particularly the shift to using JSON objects, mark a significant evolution in how developers interact with the platform. This move aligns Cabbage with contemporary development practices, enhances user experience, and empowers users to build richer, more dynamic applications with greater ease.

#### 5. Exporting instruments

Although the process of exporting has remained largely unchanged, the sequence of events during export has undergone some updates. The most significant change is that all instrument resources are now exported to a set resource folder by default. All assets, including images, .csd files, and other related resources, will be placed in the following locations (unless you enable the 'Bundle Resources' option in the Cabbage Vs-Code settings):

* MacOS
    `/Library/CabbageAudio/PLUGIN_NAME/`
* Windows
    `C:/ProgramData/CabbageAudio/PLUGIN_NAME/`

Cabbage automatically searches these directories when it starts, so it’s essential not to move them to another location.

When sharing plugins, you must ensure that the entire resource folder is copied along with the plugin binary and restored to its correct location, as specified above, to ensure proper functionality on the target machine.

Although keeping mutable artifacts outside of the plugin bundle represents a departure from Cabbage 2, it offers several advantages:

* You avoid re-signing the plugin for every resource change
* Updates can be shipped as a simple ZIP or tarball
* No notarization is required for non-executable assets
* Faster iteration, especially during development
* A cleaner separation between code and data

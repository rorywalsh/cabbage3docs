---
title: Custom Interfaces
description: Building entirely custom web-based plugin interfaces with any framework
---

# Custom Interfaces

It's also possible to design a completely custom web-based interface using any framework you like — vanilla HTML/JS, Svelte, React, Vue, and so on. The Cabbage JS API handles all communication with the Csound backend, so your UI code stays framework-agnostic.

Unlike [Custom Widgets](./customWidgets), this approach does not use Cabbage's built-in UI editing tools. Instead, you have full control over the interface and simply use the API to exchange data with Csound.

📃 **Note:** A `<Cabbage>{...}</Cabbage>` section is still required in your `.csd` file to define the plugin parameters exposed to the host DAW. The widgets declared there are not rendered visually when a custom interface is active, but they set up the parameter slots that your UI controls map to.

## Getting Started

The quickest way to start a custom interface project is the **Export Vanilla Plugin** command in the Command Palette. This exports a working plugin binary and creates a ready-to-use resource folder alongside it containing:

- A `cabbage/` folder with `cabbage.js` and supporting files
- A starter `index.html` wired up to the Cabbage JS API (can be removed in using a build tool to generate a user-defined index.html)
- A `cabbage.project.json` configured for local file mode

From inside that resource folder you can initialise your framework project of choice:

```bash
# Svelte / Vite
npm create vite@latest MyPlugin -- --template svelte
cd MyPlugin && npm install

# React / Vite
npm create vite@latest MyPlugin -- --template react
cd MyPlugin && npm install
```

Then update `cabbage.project.json` to point at the dev server while developing, and switch back to the built output for distribution:

```jsonc
// Development — point at the running dev server:
{ "entry": "http://localhost:5173" }

// Production — point at the built output:
// { "entry": "MyPlugin/dist/index.html" }
```

## VS Code Development Workflow

The Cabbage VS Code extension can load your custom interface directly in the webview panel, replacing the native widget UI. This lets you develop and test your interface alongside the Csound instrument without leaving VS Code.

### Setting up `cabbage.project.json`

Create a `cabbage.project.json` file in the same folder as your `.csd` file using the **Create Cabbage Project File** command from the Command Palette. This tells the extension how to load your UI:

```jsonc
{
  // Point to a running dev server (e.g. Vite) for live-reload during development:
  "entry": "http://localhost:5173"

  // Or point to a built HTML file for plain HTML or production builds:
  // "entry": "dist/index.html"
}
```

When you save the `.csd` file, the extension reads this config and loads your interface in the webview panel at the correct size (taken from the `form` widget's `size` in the `<Cabbage>` section).

### Dev Server Mode (Vite / React / Svelte)

When `entry` is a `http://` URL, the extension wraps the dev server in an iframe relay. This means:
- Hot module replacement (HMR) works as normal — changes in your framework project appear instantly
- Two-way communication with the Csound backend is fully supported via `window.parent.postMessage`, handled transparently by the Cabbage JS API
- The Vite dev server must already be running before you save the `.csd`

#### Configuring the `cabbage.js` path

A typical Cabbage project has `cabbage.js` in a `cabbage/` folder alongside the `.csd`, with the framework project in a subdirectory:

```
MyPlugin/
├── MyPlugin.csd
├── cabbage.project.json
├── cabbage/
│   └── cabbage.js          ← the Cabbage JS API
└── MyPlugin/               ← Vite / React / Svelte project
    ├── vite.config.js
    └── src/
```

Because `cabbage.js` lives outside the framework project directory, bundlers can't resolve it with a plain relative import like `'../cabbage/cabbage.js'` without a little configuration. Add a path alias and allow the dev server to serve files from the parent directory:

**`vite.config.js`:**
```javascript
import { defineConfig } from 'vite';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

export default defineConfig({
  resolve: {
    alias: {
      // 'cabbage' resolves to cabbage.js in the parent project folder
      cabbage: path.resolve(__dirname, '../cabbage/cabbage.js')
    }
  },
  server: {
    fs: {
      // Allow the dev server to serve files from outside the project root
      allow: ['..']
    }
  }
});
```

With this in place, you can import the API with a clean bare specifier anywhere in your project:

```javascript
import { Cabbage } from 'cabbage';
```

### File Mode (Plain HTML / Built Output)

When `entry` is a relative file path, the extension loads the HTML file directly in the webview. This works for:
- Vanilla HTML/JS projects
- Built output from a framework (e.g., `dist/index.html` after `npm run build`)

## Communication

Import the Cabbage API from `cabbage.js`:

```javascript
import { Cabbage } from './cabbage/cabbage.js';  // vanilla HTML
// or, with a bundler alias:
import { Cabbage } from 'cabbage';               // Vite / webpack
```

### Sending Data (UI → Backend)

Use `Cabbage.sendControlData()` to send parameter values to Csound:

```javascript
Cabbage.sendControlData({ channel: "frequency", value: 1000, gesture: "complete" }, null);
```

For continuous controls (sliders, XY pads), use the gesture sequence to support DAW automation recording:

```javascript
slider.addEventListener('pointerdown', () =>
    Cabbage.sendControlData({ channel: "gain", value: slider.value, gesture: "begin" }, null));
slider.addEventListener('input', () =>
    Cabbage.sendControlData({ channel: "gain", value: slider.value, gesture: "value" }, null));
slider.addEventListener('pointerup', () =>
    Cabbage.sendControlData({ channel: "gain", value: slider.value, gesture: "end" }, null));
```

### Receiving Data (Backend → UI)

Use `Cabbage.addMessageListener()` to handle all incoming messages. It works in every environment — VS Code, DAW plugin, dev server iframe — without any environment-specific setup:

```javascript
Cabbage.addMessageListener((msg) => {
    if (msg.command === 'parameterChange') {
        // DAW automation or host parameter change.
        // paramIdx/value may be top-level or nested in msg.data depending on the host.
        const data = msg.data ?? msg;
        updateControl(data.paramIdx, data.value);
    } else if (msg.command === 'widgetUpdate') {
        // Value update from cabbageSetValue opcode — id and value are top-level.
        if (msg.value !== undefined) {
            document.getElementById(msg.id).value = msg.value;
        }
    }
});
```

`addMessageListener` returns a cleanup function — useful in frameworks with component lifecycle hooks.

> **Avoid feedback loops**: When handling `parameterChange`, update the visual display only. Never call `sendControlData()` in response — it creates a loop that interferes with DAW automation.

## Examples

### Vanilla HTML

A complete two-slider example:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Plugin</title>
</head>
<body>
    <input type="range" id="slider1" min="0" max="1000" value="0">
    <input type="range" id="slider2" min="0" max="1000" value="0">

    <script type="module">
        import { Cabbage } from './cabbage/cabbage.js';

        const isDragging = { slider1: false, slider2: false };

        ['slider1', 'slider2'].forEach((id) => {
            const slider = document.getElementById(id);
            slider.addEventListener('pointerdown', () => {
                isDragging[id] = true;
                Cabbage.sendControlData({ channel: id, value: +slider.value, gesture: 'begin' }, null);
            });
            slider.addEventListener('input', () => {
                if (isDragging[id])
                    Cabbage.sendControlData({ channel: id, value: +slider.value, gesture: 'value' }, null);
            });
            slider.addEventListener('pointerup', () => {
                isDragging[id] = false;
                Cabbage.sendControlData({ channel: id, value: +slider.value, gesture: 'end' }, null);
            });
            slider.addEventListener('pointercancel', () => { isDragging[id] = false; });
        });

        Cabbage.addMessageListener((msg) => {
            const data = msg.data ?? msg;
            if (msg.command === 'parameterChange') {
                const id = data.paramIdx === 0 ? 'slider1' : 'slider2';
                if (!isDragging[id]) document.getElementById(id).value = data.value;
            } else if (msg.command === 'widgetUpdate' && !isDragging[msg.id]) {
                const el = document.getElementById(msg.id);
                if (el && msg.value !== undefined) el.value = msg.value;
            }
        });
    </script>
</body>
</html>
```

### Svelte

```svelte
<script>
  import { Cabbage } from 'cabbage';
  import { onMount, onDestroy } from 'svelte';

  let value = $state(0);
  let removeListener;

  onMount(() => {
    removeListener = Cabbage.addMessageListener((msg) => {
      if (msg.command === 'widgetUpdate' && msg.id === 'myChannel') {
        value = msg.value;
      } else if (msg.command === 'parameterChange') {
        const data = msg.data ?? msg;
        if (data.paramIdx === 0) value = data.value;
      }
    });
  });

  onDestroy(() => removeListener?.());

  const onChange = (e) => {
    value = +e.target.value;
    Cabbage.sendControlData({ channel: 'myChannel', value, gesture: 'complete' }, null);
  };
</script>

<input type="range" min="0" max="1" step="0.01" value={value} oninput={onChange}>
```

### React

```jsx
import { useEffect, useState } from 'react';
import { Cabbage } from 'cabbage';

export function MyControl() {
  const [value, setValue] = useState(0);

  useEffect(() => {
    const remove = Cabbage.addMessageListener((msg) => {
      if (msg.command === 'widgetUpdate' && msg.id === 'myChannel') {
        setValue(msg.value);
      }
    });
    return remove; // React calls this on unmount
  }, []);

  const onChange = (e) => {
    const v = +e.target.value;
    setValue(v);
    Cabbage.sendControlData({ channel: 'myChannel', value: v, gesture: 'complete' }, null);
  };

  return <input type="range" min={0} max={1} step={0.01} value={value} onChange={onChange} />;
}
```


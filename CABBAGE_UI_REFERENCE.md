# Cabbage UI JSON Reference

**Purpose:** LLM prompt reference for generating valid Cabbage JSON widgets. Zero fluff, exact syntax only.

---

## Global Structure

Root JSON must contain `widgets` array. Optional top-level config properties outside `widgets`.

```json
<Cabbage>{
  "pluginId": "MyPl",
  "channelConfig": [{"name": "Stereo", "ins": "2", "outs": "2"}],
  "enableDevTools": true,
  "logger": {"enabled": true, "file": "debug.log", "replace": false},
  "package": {"include": [{"src": "samples", "dest": "samples"}], "cabzOutputDir": ""},
  "widgets": [...]
}</Cabbage>
```

**pluginId:** Required. 4 chars auto-prefixed with `com.cabbageaudio.` or full reversed domain.  
**channelConfig:** Array of `{"name": string, "ins": string, "outs": string}` objects.  
**enableDevTools:** `true|false` - enables dev tools in plugin mode.  
**logger:** Optional logging config with `enabled`, `file`, `replace` fields.  
**package:** Optional. Array of `{"src": path, "dest": dir}` for resource bundling.

---

## Widget Channel System

Widgets use `channels` array for value communication. Each channel has:
- **id:** Unique channel name (used by `cabbageGetValue`/`cabbageSetValue`)
- **label:** Optional human-readable name for DAW display (defaults to id)
- **eventType:** Event trigger type (defaults to `valueChanged`)
- **type:** `"number"|"string"` (defaults to `number`)
- **range:** Min/max/default/skew/increment object

```json
"channels": [{
  "id": "gain",
  "label": "Gain Control",
  "eventType": "valueChanged",
  "type": "number",
  "range": {"min": 0, "max": 1, "defaultValue": 0.5, "skew": 1, "increment": 0.001}
}]
```

**Valid eventType values:**
- `valueChanged` (default)
- `mousePressLeft`, `mousePressRight`, `mousePressMiddle`
- `mouseMoveX`, `mouseMoveY`
- `mouseDragX`, `mouseDragY`
- `mouseInside`

**Top-level id:** Optional. Used for UI updates via `cabbageSet`. If omitted, defaults to `channels[0].id`.

---

## Common Properties (All Widgets)

```json
"active": true,
"automatable": true,
"bounds": {"left": 0, "top": 0, "width": 100, "height": 100},
"id": "widgetId",
"persistence": {"preset": true, "session": true},
"visible": true,
"zIndex": 1
```

**active:** `true|false` - if false, widget is deactivated but updateable from Csound.  
**automatable:** `true|false` - if true, appears as DAW parameter. Cannot change dynamically.  
**bounds:** Position/size in pixels. All integers.  
**id:** Top-level channel for UI updates. Optional, defaults to `channels[0].id`.  
**persistence:** `preset` and `session` both `true|false`. Auto-cascades if `preset: false`.  
**visible:** `true|false` - widget visibility.  
**zIndex:** Integer. Higher values render on top.

---

## Form

Main application window. Must have exactly one per instrument. Reserved channel: `MainForm`.

```json
{
  "type": "form",
  "caption": "Window Title",
  "size": {"width": 600, "height": 400},
  "id": "MainForm",
  "style": {
    "fill": "#004c6b",
    "opacity": 1
  }
}
```

**caption:** Window title (standalone mode only).  
**size:** `{"width": int, "height": int}`. Defaults to 600x300.  
**style.fill:** Background color.

---

## Button

Toggle or momentary button.

```json
{
  "type": "button",
  "bounds": {"left": 10, "top": 10, "width": 100, "height": 30},
  "channels": [{"id": "trigger", "event": "valueChanged"}],
  "label": {"text": {"off": "Start", "on": "Stop"}, "offsetY": 0},
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 0,
    "borderColor": "#dddddd",
    "on": {"backgroundColor": "#3d800a", "textColor": "#dddddd"},
    "off": {"backgroundColor": "#3d800a", "textColor": "#dddddd"},
    "hover": {"backgroundColor": "#4ca10c", "textColor": "#dddddd"},
    "active": {"backgroundColor": "#2d6008", "textColor": "#dddddd"}
  }
}
```

**label.text:** `{"off": string, "on": string}` or single string.  
**label.offsetY:** Vertical offset for external label.  
**style:** States are `on`, `off`, `hover`, `active`. Each has `backgroundColor`, `textColor`.

---

## CheckBox

Toggle checkbox.

```json
{
  "type": "checkBox",
  "bounds": {"left": 10, "top": 10, "width": 120, "height": 20},
  "channels": [{"id": "enable"}],
  "label": {"text": "Enable", "offsetY": 0},
  "value": 0,
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "on": {"backgroundColor": "#3d800a", "checkColor": "#ffffff"},
    "off": {"backgroundColor": "#ffffff", "checkColor": "#000000"}
  }
}
```

**value:** Initial state (0 or 1).

---

## ComboBox

Dropdown list. Returns selected index (0-based).

```json
{
  "type": "comboBox",
  "bounds": {"left": 10, "top": 10, "width": 150, "height": 30},
  "channels": [{"id": "selection"}],
  "items": ["Option 1", "Option 2", "Option 3"],
  "populate": {
    "directories": ["path/to/dir"],
    "fileType": "*.wav;*.mp3",
    "fullFileAndPath": false,
    "order": "date",
    "labelWhenEmpty": "No Files",
    "defaultLabel": ""
  },
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "backgroundColor": "#ffffff",
    "textColor": "#000000",
    "fontFamily": "Verdana",
    "fontSize": 14
  }
}
```

**items:** Array of strings. Index sent to channel. Mutually exclusive with `populate`.  
**populate.order:** `"date"|"size"|"alphabetically"`.  
**populate.fileType:** Wildcard pattern (e.g., `"*.txt;*.csv"`).

---

## FileButton

Opens file browser. Returns file path as string.

```json
{
  "type": "fileButton",
  "bounds": {"left": 10, "top": 10, "width": 100, "height": 30},
  "channels": [{"id": "filePath", "type": "string"}],
  "label": {"text": "Load File", "offsetY": 0},
  "directory": "/default/path",
  "filters": "*.wav;*.aif;*.mp3",
  "mode": "file",
  "openAtLastKnownLocation": true,
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "backgroundColor": "#3d800a",
    "textColor": "#ffffff"
  }
}
```

**mode:** `"file"|"directory"`.  
**filters:** Wildcard pattern. Use `"*"` for all files.  
**openAtLastKnownLocation:** `true|false`. If false, uses `directory` value.

---

## GenTable

Displays function table or audio file waveform.

```json
{
  "type": "genTable",
  "bounds": {"left": 10, "top": 10, "width": 400, "height": 200},
  "id": "gentable1",
  "channels": [{"id": "tableUpdate"}],
  "tableNumber": 1,
  "file": "path/to/audio.wav",
  "sampleRange": {"start": 0, "end": -1},
  "range": {"min": -1, "max": 1},
  "selectableRegions": {"enabled": false, "channel": "regionSelect"},
  "label": {"text": "Waveform", "offsetY": 0},
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "fill": "#93d200",
    "background": "#00000022"
  }
}
```

**tableNumber:** Csound function table number.  
**file:** Audio file path (mutually exclusive with `tableNumber` for source).  
**sampleRange:** `{"start": int, "end": int}`. Use -1 for end to include all samples.  
**selectableRegions.enabled:** `true|false`. If true, users can select waveform regions.

---

## GroupBox

Visual container for organizing widgets.

```json
{
  "type": "groupBox",
  "bounds": {"left": 10, "top": 10, "width": 300, "height": 200},
  "id": "controlGroup",
  "label": {"text": "Controls", "offsetY": 0},
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "fill": "#888888"
  }
}
```

**Note:** Background becomes transparent when children are present.

---

## HorizontalSlider

Horizontal slider control.

```json
{
  "type": "horizontalSlider",
  "bounds": {"left": 10, "top": 10, "width": 300, "height": 40},
  "channels": [{
    "id": "gain",
    "range": {"min": 0, "max": 1, "defaultValue": 0.5, "skew": 1, "increment": 0.001}
  }],
  "label": {"text": "Gain", "offsetY": 0},
  "popup": 1,
  "valueText": {"visible": true, "width": "auto", "prefix": "", "postfix": " dB"},
  "style": {
    "opacity": 1,
    "thumb": {
      "width": "auto",
      "height": "auto",
      "backgroundColor": "#0295cf",
      "borderColor": "#525252",
      "borderWidth": 2,
      "borderRadius": 4
    },
    "track": {
      "width": "auto",
      "fillColor": "#93d200",
      "backgroundColor": "#ffffff"
    },
    "label": {
      "fontFamily": "Verdana",
      "fontSize": "auto",
      "fontColor": "#dddddd",
      "textAlign": "center"
    },
    "valueText": {
      "fontFamily": "Verdana",
      "fontSize": "auto",
      "fontColor": "#dddddd"
    }
  }
}
```

**popup:** `0|1` - show popup value on drag.  
**valueText.visible:** `true|false` - show inline value editor.  
**valueText.width:** Integer or `"auto"`.  
**style values:** `"auto"` calculated from bounds.

---

## VerticalSlider

Vertical slider control. Identical structure to `horizontalSlider`.

```json
{
  "type": "verticalSlider",
  "bounds": {"left": 10, "top": 10, "width": 40, "height": 300},
  "channels": [{
    "id": "volume",
    "range": {"min": 0, "max": 1, "defaultValue": 0.8, "skew": 1, "increment": 0.001}
  }],
  "label": {"text": "Volume", "offsetY": 0},
  "popup": 1,
  "valueText": {"visible": true, "width": "auto", "prefix": "", "postfix": ""},
  "style": { /* Same as horizontalSlider */ }
}
```

---

## RotarySlider

Rotary/knob slider control.

```json
{
  "type": "rotarySlider",
  "bounds": {"left": 10, "top": 10, "width": 80, "height": 90},
  "channels": [{
    "id": "cutoff",
    "range": {"min": 20, "max": 20000, "defaultValue": 1000, "skew": 0.5, "increment": 1}
  }],
  "label": {"text": "Cutoff", "offsetY": 0},
  "popup": 1,
  "valueText": {"visible": true, "width": "auto", "prefix": "", "postfix": " Hz"},
  "filmStrip": {"file": "path/to/filmstrip.png", "frames": 100},
  "style": {
    "opacity": 1,
    "thumb": {
      "radius": "auto",
      "backgroundColor": "#0295cf",
      "borderColor": "#525252",
      "borderWidth": 2
    },
    "track": {
      "width": "auto",
      "fillColor": "#93d200",
      "backgroundColor": "#393939ff"
    },
    "label": {
      "fontFamily": "Verdana",
      "fontSize": "auto",
      "fontColor": "#dddddd",
      "textAlign": "center"
    },
    "valueText": {
      "fontFamily": "Verdana",
      "fontSize": "auto",
      "fontColor": "#aaaaaa"
    }
  }
}
```

**filmStrip:** Optional. `{"file": path, "frames": int}` - use filmstrip image instead of default rendering.

---

## NumberSlider

Numeric value with click-drag adjustment.

```json
{
  "type": "numberSlider",
  "bounds": {"left": 10, "top": 10, "width": 80, "height": 25},
  "channels": [{
    "id": "tempo",
    "range": {"min": 20, "max": 300, "defaultValue": 120, "skew": 1, "increment": 1}
  }],
  "valueTextBox": {
    "visible": true,
    "prefix": "",
    "postfix": " BPM",
    "decimalPlaces": 0
  },
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "backgroundColor": "#ffffff",
    "textColor": "#000000",
    "fontFamily": "Verdana",
    "fontSize": 14
  }
}
```

**valueTextBox.decimalPlaces:** Integer. Controls display precision.

---

## OptionButton

Cycles through items array. Returns index.

```json
{
  "type": "optionButton",
  "bounds": {"left": 10, "top": 10, "width": 100, "height": 30},
  "channels": [{"id": "waveform"}],
  "items": ["Sine", "Square", "Saw", "Triangle"],
  "populate": { /* Same as comboBox */ },
  "style": {
    "opacity": 1,
    "borderRadius": 4,
    "borderWidth": 1,
    "borderColor": "#dddddd",
    "backgroundColor": "#3d800a",
    "textColor": "#ffffff",
    "fontFamily": "Verdana",
    "fontSize": 14
  }
}
```

---

## XyPad

2D XY pad controller with independent X/Y channels.

```json
{
  "type": "xyPad",
  "bounds": {"left": 10, "top": 10, "width": 300, "height": 300},
  "channel": {"id": "xyPad1", "x": "freqX", "y": "filterY"},
  "range": {
    "x": {"min": 100, "max": 10000, "defaultValue": 1000, "skew": 1, "increment": 0.001},
    "y": {"min": 0, "max": 1, "defaultValue": 0.5, "skew": 1, "increment": 0.001}
  },
  "text": {"x": "Frequency", "y": "Resonance"},
  "ballSize": 20,
  "label": {"text": "XY Control", "offsetY": 0},
  "popup": 1,
  "style": {
    "opacity": 1,
    "ball": {
      "backgroundColor": "#0295cf",
      "borderColor": "#ffffff",
      "borderWidth": 2
    },
    "background": "#000000",
    "gridColor": "#333333"
  }
}
```

**channel:** `{"id": topLevelId, "x": xChannelName, "y": yChannelName}`.  
**range:** Separate range objects for `x` and `y`.  
**text:** Axis labels `{"x": string, "y": string}`.  
**ballSize:** Ball diameter in pixels.

---

## Keyboard

MIDI keyboard widget.

```json
{
  "type": "keyboard",
  "bounds": {"left": 10, "top": 10, "width": 600, "height": 100},
  "id": "keyboard",
  "channels": [{"id": "keyboard"}],
  "value": 48,
  "keyWidth": 24,
  "color": {
    "whiteKey": "#ffffff",
    "blackKey": "#000000",
    "keyDown": "#93d200"
  },
  "style": {
    "opacity": 1
  }
}
```

**value:** Leftmost key MIDI note number.  
**keyWidth:** White key width in pixels.  
**color:** Keyboard colors configured here, NOT in `style`.

---

## Image

Display image or interact via mouse events.

```json
{
  "type": "image",
  "bounds": {"left": 10, "top": 10, "width": 200, "height": 200},
  "id": "bgImage",
  "channels": [{
    "id": "imageClick",
    "event": "mousePressLeft"
  }],
  "file": "path/to/image.png",
  "style": {
    "opacity": 1,
    "borderRadius": 0,
    "borderWidth": 0,
    "borderColor": "#dddddd"
  }
}
```

**file:** Path to image file (PNG, JPG, SVG, etc.).

---

## Label

Static or interactive text label.

```json
{
  "type": "label",
  "bounds": {"left": 10, "top": 10, "width": 200, "height": 30},
  "id": "titleLabel",
  "label": {"text": "Title Text", "offsetY": 0},
  "style": {
    "opacity": 1,
    "borderRadius": 0,
    "borderWidth": 0,
    "borderColor": "#dddddd",
    "backgroundColor": "transparent",
    "textColor": "#ffffff",
    "fontFamily": "Verdana",
    "fontSize": 16,
    "textAlign": "left"
  }
}
```

**style.textAlign:** `"left"|"center"|"right"`.

---

## Color Format

All color properties accept:
- **Hex:** `#RRGGBB` or `#RRGGBBAA`
- **RGB/RGBA:** `rgb(r, g, b)` or `rgba(r, g, b, a)`
- **Named CSS colors:** `"red"`, `"blue"`, `"transparent"`, etc.

---

## Auto Values

`"auto"` in style properties means calculated from widget bounds. Common in:
- `thumb.width`, `thumb.height`, `thumb.radius`
- `track.width`
- `fontSize`
- `valueText.width`

---

## Critical Rules

1. **Never set `range.value` explicitly** - it's auto-populated during runtime. Use `defaultValue` instead.
2. **Top-level `id` vs `channels[].id`:** Use top-level `id` for UI updates (`cabbageSet`), channel `id` for values (`cabbageSetValue`).
3. **Auto-cascade:** Setting `persistence.preset: false` auto-sets `session: false` unless explicitly overridden.
4. **Increment behavior:** 
   - `increment >= 1.0`: DAW shows discrete steps
   - `increment < 1.0`: DAW shows continuous slider
   - Cabbage always quantizes to increment before sending to Csound
5. **Form requirements:** Exactly one form per instrument, reserved channel `MainForm`.
6. **Channel names:** Can contain spaces and don't need to start with a letter (Cabbage 3).
7. **File paths:** Can be relative to .csd file or absolute.

---

## END OF REFERENCE

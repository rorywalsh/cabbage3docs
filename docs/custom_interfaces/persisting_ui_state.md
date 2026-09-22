---
title: Persisting Custom UI State
description: Keep custom interface state across UI teardown using string channels
---

# Persisting Custom UI State

The plugin host destroys and recreates your web interface whenever it sees fit — closing and reopening the plugin window, switching views, reloading a DAW session. All JavaScript state is lost each time. The Cabbage backend, however, holds widget and channel state across UI lifetimes and re-pushes it every time the UI loads. This page shows how to ride that mechanism to persist arbitrary custom UI state (a patcher graph, a sequencer pattern, editor settings) with no files involved.

The pattern, in brief:

1. Declare a hidden holder widget with a **string channel** in your `.csd`.
2. Push serialized state into it with `sendControlData()` whenever things change.
3. Rebuild your UI from it when the launch dumps arrive.

The framework's own `comboBox` widget uses exactly this loop to remember its selected item.

## 1. Declare a hidden string channel

Any widget can carry the state; an invisible, inactive `label` keeps it out of the way:

```json
{
    "type": "label",
    "channels": [{ "id": "myUiState", "type": "string" }],
    "bounds": { "top": 0, "left": 0, "width": 0, "height": 0 },
    "visible": false,
    "active": false,
    "label": { "text": "" }
}
```

The `"type": "string"` on the channel is load-bearing, not decorative. The backend treats string channels as first-class state: it creates a Csound string channel for them, keeps the latest value in `channels[0].stringValue`, and includes it in session and preset saves. Without it, the channel is handled as numeric and your text will not round-trip.

## 2. Push state on change

`sendControlData()` accepts string values. On a non-automatable channel the backend stores the string as the channel's `stringValue` (and into the matching Csound string channel, so your orchestra can read it too):

```js
import { Cabbage } from './cabbage/cabbage.js';

let lastSent = '';
let saveTimer = null;

function pushState(stateObj) {
    const json = JSON.stringify(stateObj);
    if (json === lastSent) return; // echo suppression: skip unchanged state
    lastSent = json;
    Cabbage.sendControlData({ channel: 'myUiState', value: json }, null);
}

// Debounce: UI events (drags, keystrokes) fire far more often than worth saving.
store.subscribe((state) => {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => pushState(state), 300);
});
```

## 3. Restore on launch

Register your listener **before** signalling ready — the backend sends the current widget state (full `widgetJson` dumps, possibly one `batchWidgetUpdate`) in response to `cabbageIsReadyToLoad`. Find your channel's `stringValue` in the dumps and rebuild:

```js
function readState(entry) {
    try {
        const w = Cabbage.parseWidgetJson(entry.widgetJson);
        const ch = (w.channels || []).find((c) => c && c.id === 'myUiState');
        if (ch && typeof ch.stringValue === 'string' && ch.stringValue) {
            return JSON.parse(ch.stringValue);
        }
    } catch (e) { /* fall through: no saved state */ }
    return null;
}

Cabbage.addMessageListener((msg) => {
    const data = msg.data ?? msg;
    if (msg.command === 'widgetUpdate' && (data?.id ?? data?.channel) === 'myUiState') {
        rebuildUi(readState(data)); // null => first launch, keep your defaults
    } else if (msg.command === 'batchWidgetUpdate') {
        for (const w of msg.widgets ?? []) {
            const entry = w.data ?? w;
            if ((entry?.id ?? entry?.channel) === 'myUiState') {
                rebuildUi(readState(entry));
                break;
            }
        }
    }
});

Cabbage.sendCustomCommand('cabbageIsReadyToLoad', null);
```

## 4. Two traps to avoid

**Echo loops.** Rebuilding your UI fires your own change handlers, which push state back. Always compare against the last sent (or last restored) snapshot and skip identical payloads, as in the `lastSent` check above.

**Seed clobbers save.** Your change handlers fire for the default/seeded UI too — typically before the saved state has arrived. Gate outbound pushes until the first launch dumps have been seen (plus a short timeout fallback), so the seed can never overwrite the saved snapshot:

```js
let backendStateKnown = false;
setTimeout(() => { backendStateKnown = true; }, 1500);
// ...set backendStateKnown = true when the first widgetUpdate/batch arrives...
// ...only push when backendStateKnown is true...
```

## Orchestra access (optional)

Because the value also lands in a Csound string channel, your instrument can participate: read it with the string variant of `cabbageGetValue` (the trigger version fires only when the text changes), parse it with the [`cabbageJsonGet`](../cabbage_opcodes/cabbageJsonGet) family of opcodes, and write widget text back with the string form of `cabbageSet`:

```csound
state:S, trig:k = cabbageGetValue("myUiState")
if trig == 1 then
    cabbageSet(trig, "myUiState", "label.text", state)
endif
```

To read fields out of the restored JSON, query it directly — [`cabbageJsonGet`](../cabbage_opcodes/cabbageJsonGet) for values (string, numeric, and array overloads), [`cabbageJsonType`](../cabbage_opcodes/cabbageJsonType) to branch on value types, [`cabbageJsonHas`](../cabbage_opcodes/cabbageJsonHas) / [`cabbageJsonLen`](../cabbage_opcodes/cabbageJsonLen) for existence and sizes, and [`cabbageJsonSet`](../cabbage_opcodes/cabbageJsonSet) to patch documents in the orchestra:

```csound
state:S, trig:k = cabbageGetValue("myUiState")
if trig == 1 then
    freq:k = cabbageJsonGet(state, "nodes.0.params.freq")
endif
```

This is the right tool when Csound needs to transform or react to the state. For pure UI state that Csound never reads, skip the orchestra entirely — the `sendControlData` → `stringValue` → launch-dump loop needs no instrument code.

## See also

- [Cabbage JS API](./CabbageJS_API) — `sendControlData`, `addMessageListener`, `extractValue`
- [Saving and Loading State](../using_cabbage/saving_and_loading_state) — file presets and the `persistence` flags that control what session/preset save includes
- [cabbageGetValue](../cabbage_opcodes/cabbageGetValue) and [cabbageSet](../cabbage_opcodes/cabbageSet) — string variants for orchestra-side access

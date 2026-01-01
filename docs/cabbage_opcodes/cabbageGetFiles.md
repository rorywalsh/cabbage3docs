# cabbageGetFiles

Returns a list of files in a directory optionally filtered by extension. Useful for populating file lists for widgets (e.g., comboboxes) or for scanning resource folders.

## Syntax

SFiles[] **cabbageGetFiles** SDirectory, SFileType

## Initialization

- `SDirectory` – string: The directory to search. May be an absolute path or relative to the current CSD directory.
- `SFileType` – string (optional): A single extension (e.g. `.json`) or a semicolon-separated list (e.g. `.wav;.mp3`). If empty, all files are returned.

The opcode returns an array of strings containing absolute file paths (forward-slash separators) matching the filter.

## Example

```cs
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    ; Get all JSON presets from the presets folder
    files:S[] = cabbageGetFiles("/Users/me/Presets", ".json")
    i = 0
    while i < len(files) do
        prints("%s\n", files[i])
        i += 1
    od
endin
```

## Notes

- If the directory does not exist an error is logged and an empty array is returned.
- Paths are normalized to use forward slashes (`/`) regardless of platform.
- Use the `USER_*_DIRECTORY` reserved channels in combination with this opcode to access platform-specific folders without hardcoding paths.

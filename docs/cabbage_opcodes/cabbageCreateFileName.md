# cabbageCreateFileName

Generates a likely-unique filename in a target directory using the requested extension. This opcode is useful when you need a valid and unique filename for testing. It opcode returns a full path (forward slashes) but does not create the file on disk. This opcode is i-time only, so it's best used in a dedicated instrument that will generate the filename when needed. 

## Syntax

SFilename **cabbageCreateFileName** SDirectory, SExtension

## Initialization

- `SDirectory` – string: Target directory for the new filename. May be absolute or relative to the current CSD.
- `SExtension` – string: File extension including the leading dot, e.g. `.json`.

The opcode returns a single string containing a full path that is intended not to collide with existing files in `directory`.

## Example

```cs
ksmps = 32
nchnls = 2
0dbfs = 1

instr 1
    dir:S = chnget("USER_DOCUMENTS_DIRECTORY")
    fname:S = cabbageCreateFileName(dir, ".json")
    prints("New filename: %s\n", fname)
endin
```

## Notes

- The returned filename is not created by this opcode; use standard file IO to write data to the path if desired.
- Use reserved `USER_*_DIRECTORY` channels to choose platform-appropriate storage locations.

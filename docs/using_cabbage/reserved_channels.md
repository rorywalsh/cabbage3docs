# Reserved Channels

Reserved channels in Cabbage 3 are special string channels that are automatically populated by the Cabbage engine with system-specific directory paths. These channels provide a cross-platform way to access common system directories without hardcoding paths. Cabbage 3 works with absolute file paths, so be sure to derive all file paths from known locations.  

## Available Reserved Channels

### CSD_PATH
The directory path where the current CSD file is located. Useful for loading resources relative to your CSD file location.

### IS_A_PLUGIN
Returns 1 if the instrument is running inside a DAW, otherwise returns 0. 

### USER_HOME_DIRECTORY
The user's home directory. On Windows, this is typically `C:\Users\<username>`. On macOS and Linux, this is `/Users/<username>` or `/home/<username>` respectively.

### USER_DOCUMENTS_DIRECTORY
The user's Documents folder. On Windows, this is `C:\Users\<username>\Documents`. On macOS, this is `/Users/<username>/Documents`. On Linux, this defaults to the home directory since Linux doesn't have a standard Documents folder.

### USER_DESKTOP_DIRECTORY
The user's Desktop folder. On Windows, this is `C:\Users\<username>\Desktop`. On macOS, this is `/Users/<username>/Desktop`. On Linux, this is `/home/<username>/Desktop`.

### USER_MUSIC_DIRECTORY
The user's Music folder. On Windows, this is `C:\Users\<username>\Music`. On macOS, this is `/Users/<username>/Music`. On Linux, this is `/home/<username>/Music`.

### USER_MOVIES_DIRECTORY
The user's Movies/Videos folder. On Windows, this is `C:\Users\<username>\Videos`. On macOS, this is `/Users/<username>/Movies`. On Linux, this is `/home/<username>/Videos`.

### USER_PICTURES_DIRECTORY
The user's Pictures folder. On Windows, this is `C:\Users\<username>\Pictures`. On macOS, this is `/Users/<username>/Pictures`. On Linux, this is `/home/<username>/Pictures`.

### USER_APPLICATION_DATA_DIRECTORY
The user's application data directory for storing application-specific data. On Windows, this is `C:\Users\<username>\AppData\Local`. On macOS, this is `/Users/<username>/Library/Application Support`. On Linux, this is `/home/<username>/.config`.

### COMMON_APPLICATION_DATA_DIRECTORY
The system-wide application data directory for shared application data. On Windows, this is `C:\ProgramData`. On macOS, this is `/Library/Application Support`. On Linux, this is `/opt`.

### COMMON_DOCUMENTS_DIRECTORY
The system-wide shared documents directory. On Windows, this is `C:\Users\Public\Documents`. On macOS, this is `/Users/Shared`. On Linux, this is `/usr/share`.

### WINDOWS_SYSTEM_DIRECTORY
The Windows system directory. On Windows, this is `C:\Windows\System32`. Not applicable on macOS and Linux (returns empty string).

### GLOBAL_APPLICATIONS_DIRECTORY
The system-wide applications directory. On Windows, this is `C:\Program Files`. On macOS, this is `/Applications`. On Linux, this is `/usr`.

### WINDOW_WIDTH
The width in pixels of the current Cabbage UI window. This reflects the window size available to the UI and can be used to scale or position widgets.

### WINDOW_HEIGHT
The height in pixels of the current Cabbage UI window. Use together with `WINDOW_WIDTH` to determine available drawing area.


## Usage Example

```csound
instr 1
    home:S = chnget("USER_HOME_DIRECTORY")
    desktop:S = chnget("USER_DESKTOP_DIRECTORY")
    prints("Home: %s\n", home)
    prints("Desktop: %s\n", desktop)
endin
```

## Notes

- All paths use forward slashes (`/`) as directory separators, even on Windows
- Empty strings are returned for channels that don't apply to the current platform. For example `WINDOWS_SYSTEM_DIRECTORY` will return an empty string on MacOS/Linux. 
- These channels should be treated as read-only and are automatically set by Cabbage at startup
- The actual paths may vary depending on system configuration and user settings

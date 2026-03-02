# DCS Mission (.miz) File Format Research

DCS (Digital Combat Simulator) mission files with the `.miz` extension are standard ZIP archives. They contain all the data necessary to run a mission, including the mission logic, options, localization strings, and multimedia resources.

## 1. Directory Structure

A typical `.miz` file contains the following root entries:

- `mission`: A large Lua file containing the main mission definition (units, triggers, waypoints, etc.).
- `options`: A Lua file containing mission-specific options (labels, difficulty, etc.).
- `warehouses`: A Lua file for logistics and supply data.
- `theatre`: A small text file indicating the map (e.g., `Caucasus`, `PersianGulf`).
- `l10n/`: The localization directory.
- `KNEEBOARD/`: (Optional) Custom kneeboard images.
- `Scripts/`: (Optional) Custom Lua scripts included with the mission.

## 2. Localization (l10n) System

The `l10n` folder is the core of the localization system. It contains subdirectories for each supported language.

### Supported Language Codes
- `DEFAULT`: The fallback language (usually English).
- `EN`: English.
- `CN`: Simplified Chinese.
- `RU`: Russian.
- `DE`: German.
- (Other standard ISO codes).

### Internal Structure of a Language Folder (e.g., `l10n/DEFAULT/`)
Each language folder typically contains:

1.  **`dictionary`**: A Lua file that defines a table named `dictionary`.
    - Format: `dictionary = { ["DictKey_..."] = "Text content", ... }`
    - The `mission` file references these keys instead of hardcoding strings.

2.  **`mapResource`**: A Lua file that defines a table named `mapResource`.
    - Format: `mapResource = { ["ResKey_..."] = "filename.ogg", ... }`
    - This maps resource keys used in triggers/actions to actual files located within the same language directory.

3.  **Multimedia Assets**:
    - `.ogg` / `.wav`: Voice-over files.
    - `.png` / `.jpg`: Images for briefings or triggers.
    - These files are stored directly in the language folder.

## 3. How Localization Works in DCS
- When a mission is loaded, DCS checks the user's preferred language.
- If a folder for that language exists in `l10n/`, it loads the `dictionary` and `mapResource` from there.
- If not, it falls back to `l10n/DEFAULT/`.
- Dictionary keys (e.g., `DictKey_UnitName_1`) are resolved to the strings defined in the current language's `dictionary`.
- Resource keys (e.g., `ResKey_Action_1`) are resolved to the filenames in `mapResource`, and DCS looks for those files in the corresponding language folder.

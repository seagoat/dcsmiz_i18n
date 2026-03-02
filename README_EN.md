# DCS MIZ Localization & Logic Explorer (DCSLOC)

An advanced management and analysis tool for DCS World mission files (.miz). It enables quick multi-language support and provides deep insights into the relationship between mission trigger logic and media assets.

## 🌟 Key Features

*   **Visual Side-by-Side Editing**: Compare translations across different languages with real-time search support.
*   **Global Package Scanning**: Automatically scans all internal files (mission, options, warehouses, etc.) to locate asset references.
*   **Smart Mission Tree**: Converts complex mission Lua into an interactive tree with a "Resource Focus" filtering mode.
*   **Bidirectional Linking**: Seamlessly jump between script lines and OGG/PNG assets, featuring in-game usage labels.
*   **High Performance**: Powered by Virtual Scroll technology to handle massive missions with thousands of resources smoothly.
*   **Incremental Localization**: Only packages modified content, keeping generated MIZ file sizes minimal.

## 📸 Screenshots

| Text Dictionary | Media Assets |
| :---: | :---: |
| <img src="docs/screen_text.png" width="400" alt="Text Comparison"> | <img src="docs/screen_media.png" width="400" alt="Media Asset Links"> |
| *High contrast UI with fallback tags for untranslated content.* | *Real-time audio/image preview with context subtitles attached.* |

| Mission Tree | Global Reference Scan |
| :---: | :---: |
| <img src="docs/screen_tree.png" width="400" alt="Filtered Mission Tree"> | <img src="docs/screen_links.png" width="400" alt="Bidirectional Linking"> |
| *Enable 'Focus Resources' to filter out thousands of lines of noise.* | *Usage badges show exactly which files and triggers use the asset.* |

## 🚀 Deployment & Running

### 1. Prerequisites
Ensure you have [Python 3.8+](https://www.python.org/) installed.

### 2. Start the Tool
*   **Windows Users**: Double-click `start_tool.bat` in the root directory.
*   **Manual Start**:
    ```powershell
    pip install fastapi uvicorn python-multipart
    python app_server.py
    ```

### 3. Access the Interface
Open your browser and go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 🛠 Usage Guide

### Loading a Mission
*   **Quick Select**: Choose from MIZ files in the project root.
*   **Custom Path**: Paste an absolute path from your PC and click "Load".
*   **Upload**: Click "Upload" in the top-right corner to process a new file.

### Workflow
1.  **Translate**: Compare `DEFAULT` and `CN` under the "Dictionary" category.
2.  **Verify Audio**: Switch to the `.ogg` category, play audio, and see the corresponding script displayed above.
3.  **Analyze**: Open the "Tree" view, enable "Focus Resources", and click DictKey links to jump back to the translation list.

## 📂 Project Structure
*   `app_server.py`: Web backend entry point.
*   `index.html`: High-performance SPA frontend.
*   `miz_lib.py`: Core parsing library.
*   `miz_localizer.py`: CLI incremental packaging tool.
*   `miz_browser.py`: CLI preview tool.

## ⚠️ Copyright Notice
This project is configured with `.gitignore`. **Do not upload any original or modified .miz mission files to GitHub** to protect the intellectual property of the original authors.

import zipfile
import re
import sys
import os

def parse_lua_table(content):
    """
    Simplistic parser for Lua tables like dictionary and mapResource.
    Assumes standard DCS format: ["key"] = "value",
    """
    results = {}
    # Matches: ["key"] = "value", or ["key"] = [[multi-line value]],
    # Regex for standard strings: ["(.*?)"]\s*=\s*"(.*?)"\s*,
    # Using a more robust regex for both single line and multi-line
    pattern = re.compile(r'\["(.*?)"\]\s*=\s*("(.*?)"|\[\[(.*?)\]\])\s*,', re.DOTALL)
    
    for match in pattern.finditer(content):
        key = match.group(1)
        if match.group(3) is not None:
            value = match.group(3)
        else:
            value = match.group(4)
        results[key] = value
    return results

def browse_miz(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return

    print(f"--- Browsing MIZ: {file_path} ---")
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            # 1. Identify Languages
            l10n_folders = set()
            for name in z.namelist():
                if name.startswith('l10n/'):
                    parts = name.split('/')
                    if len(parts) > 1:
                        l10n_folders.add(parts[1])
            
            print(f"Supported Languages: {', '.join(sorted(l10n_folders))}")
            
            # 2. Extract and parse data for each language
            for lang in sorted(l10n_folders):
                print(f"\nLanguage: {lang}")
                
                dict_path = f"l10n/{lang}/dictionary"
                res_path = f"l10n/{lang}/mapResource"
                
                # Dictionary Stats
                try:
                    with z.open(dict_path) as f:
                        dict_content = f.read().decode('utf-8')
                        dict_data = parse_lua_table(dict_content)
                        text_count = len(dict_data)
                        print(f"  - Dictionary entries: {text_count}")
                        # Show some examples
                        # if text_count > 0:
                        #     first_key = next(iter(dict_data))
                        #     print(f"    Example: {first_key} -> {dict_data[first_key][:50]}...")
                except KeyError:
                    print(f"  - Dictionary: Not found")
                
                # Resource Stats
                try:
                    with z.open(res_path) as f:
                        res_content = f.read().decode('utf-8')
                        res_data = parse_lua_table(res_content)
                        res_count = len(res_data)
                        print(f"  - Resource entries: {res_count}")
                        
                        # Categorize resources by file extension
                        exts = {}
                        for key, filename in res_data.items():
                            _, ext = os.path.splitext(filename.lower())
                            exts[ext] = exts.get(ext, 0) + 1
                        
                        for ext, count in exts.items():
                            type_name = "Unknown"
                            if ext in ['.ogg', '.wav']: type_name = "Audio"
                            elif ext in ['.png', '.jpg', '.jpeg']: type_name = "Image"
                            elif ext == '.lua': type_name = "Script"
                            print(f"    - {type_name} ({ext}): {count}")
                            
                        # Check if resource files actually exist in the zip
                        missing_files = []
                        for key, filename in res_data.items():
                            actual_path = f"l10n/{lang}/{filename}"
                            if actual_path not in z.namelist():
                                missing_files.append(filename)
                        
                        if missing_files:
                            print(f"    - Missing files: {len(missing_files)}")
                except KeyError:
                    print(f"  - Resources: Not found")

    except Exception as e:
        print(f"Error reading MIZ: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python miz_browser.py <path_to_miz>")
    else:
        browse_miz(sys.argv[1])

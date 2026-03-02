import zipfile
import sys
import os
import re

def parse_lua_table(content):
    """Parses DCS Lua dictionary/mapResource table."""
    results = {}
    pattern = re.compile(r'\["(.*?)"\]\s*=\s*("(.*?)"|\[\[(.*?)\]\])\s*,', re.DOTALL)
    for match in pattern.finditer(content):
        key = match.group(1)
        value = match.group(3) if match.group(3) is not None else match.group(4)
        results[key] = value
    return results

def format_lua_table(name, data):
    """Formats a Python dict back to DCS Lua table format."""
    lines = [f"{name} = \n{{"]
    for key, value in data.items():
        # Handle multi-line strings or strings containing quotes
        if "\n" in value or '"' in value:
            lines.append(f'\t["{key}"] = [[{value}]],')
        else:
            lines.append(f'\t["{key}"] = "{value}",')
    lines.append("} -- end of " + name)
    return "\n".join(lines)

def mock_translate(text):
    """Simple mock translation adding a prefix."""
    if not text.strip():
        return text
    return f"[CN] {text}"

def localize_miz(input_path, output_path, target_lang="CN"):
    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return

    print(f"--- Localizing MIZ: {input_path} -> {output_path} (Target: {target_lang}) ---")

    try:
        with zipfile.ZipFile(input_path, 'r') as zin:
            with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
                # 1. Copy all files EXCEPT those in the target l10n folder (if any)
                # and prepare for adding new l10n data
                for item in zin.infolist():
                    if not item.filename.startswith(f"l10n/{target_lang}/"):
                        zout.writestr(item, zin.read(item.filename))

                # 2. Extract DEFAULT localization data
                try:
                    def_dict_content = zin.read("l10n/DEFAULT/dictionary").decode('utf-8')
                    def_res_content = zin.read("l10n/DEFAULT/mapResource").decode('utf-8')
                    
                    def_dict = parse_lua_table(def_dict_content)
                    def_res = parse_lua_table(def_res_content)
                    
                    print(f"Found {len(def_dict)} entries in DEFAULT dictionary.")
                    
                    # 3. Create target dictionary
                    target_dict = {}
                    for key, val in def_dict.items():
                        # Here you would call a real translation API
                        target_dict[key] = mock_translate(val)
                    
                    # 4. Create target mapResource and copy assets
                    # For simplicity, we reuse the same filenames but put them in the new folder
                    target_res = def_res.copy()
                    
                    # Write the new dictionary and mapResource
                    zout.writestr(f"l10n/{target_lang}/dictionary", format_lua_table("dictionary", target_dict))
                    zout.writestr(f"l10n/{target_lang}/mapResource", format_lua_table("mapResource", target_res))
                    
                    # 5. Copy all resource files from DEFAULT to target folder
                    copied_assets = 0
                    for key, filename in def_res.items():
                        src_path = f"l10n/DEFAULT/{filename}"
                        dst_path = f"l10n/{target_lang}/{filename}"
                        
                        if src_path in zin.namelist():
                            if dst_path not in zout.namelist(): # Don't overwrite if already copied
                                zout.writestr(dst_path, zin.read(src_path))
                                copied_assets += 1
                    
                    print(f"Copied {copied_assets} assets to l10n/{target_lang}/")
                    print(f"Localization complete: {output_path}")

                except KeyError as e:
                    print(f"Critical error: Could not find base localization (DEFAULT) in the miz file. {e}")

    except Exception as e:
        print(f"Error localizing MIZ: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python miz_localizer.py <input_miz> <output_miz> [target_lang]")
    else:
        target = sys.argv[3] if len(sys.argv) > 3 else "CN"
        localize_miz(sys.argv[1], sys.argv[2], target)

import re
import json

def parse_lua_table(content):
    results = {}
    pattern = re.compile(r'\["(.*?)"\]\s*=\s*("(.*?)"|\[\[(.*?)\]\])\s*,', re.DOTALL)
    for m in pattern.finditer(content):
        results[m.group(1)] = m.group(3) if m.group(3) is not None else m.group(4)
    return results

def format_lua_table(name, data):
    if not data: return f"{name} = {{}}"
    lines = [f"{name} = \n{{"]
    for key, value in data.items():
        if "\n" in value or '"' in value:
            lines.append(f'\t["{key}"] = [[{value}]],')
        else:
            lines.append(f'\t["{key}"] = "{value}",')
    lines.append("} -- end of " + name)
    return "\n".join(lines)

def extract_usage_and_links(mission_content):
    usage, links = {}, {}
    trig_blocks = re.findall(r'\[\d+\]\s*=\s*\{(.*?)\}, -- end of \[\d+\]', mission_content, re.DOTALL)
    if not trig_blocks:
        trig_blocks = re.findall(r'\["actions"\]\s*=\s*\{(.*?)\}, -- end of \["actions"\]', mission_content, re.DOTALL)
    for b in trig_blocks:
        comment = re.search(r'\["comment"\]\s*=\s*"(.*?)"', b)
        context = comment.group(1) if comment else "Logic Block"
        found_keys = re.findall(r'(DictKey_[A-Za-z0-9_]+|ResKey_[A-Za-z0-9_]+)', b)
        for k in set(found_keys):
            if k not in usage: usage[k] = []
            if context not in usage[k]: usage[k].append(context)
        dks = re.findall(r'\["(?:subtitle|text)"\]\s*=\s*"(DictKey_[^"]+)"', b)
        rks = re.findall(r'\["file"\]\s*=\s*"(ResKey_[^"]+)"', b)
        for dk in dks:
            if dk not in links: links[dk] = []
            for rk in rks:
                if rk not in links[dk]: links[dk].append(rk)
    return usage, links

def lua_to_dict(lua_str):
    lua_str = re.sub(r'^\s*\w+\s*=\s*', '', lua_str.strip())
    lua_str = re.sub(r'--.*$', '', lua_str, flags=re.MULTILINE)
    def fix_ml(m): return '"' + m.group(1).replace('\\','\\\\').replace('"','\\"').replace('\n','\\n') + '"'
    lua_str = re.sub(r'\[\[(.*?)\]\]', fix_ml, lua_str, flags=re.DOTALL)
    lua_str = re.sub(r'\[\s*"(.*?)"\s*\]\s*=', r'"\1":', lua_str)
    lua_str = re.sub(r'\[\s*(\d+)\s*\]\s*=', r'"\1":', lua_str)
    lua_str = re.sub(r'=\s*\{', r': {', lua_str)
    lua_str = re.sub(r',\s*\}', r'}', lua_str)
    lua_str = lua_str.replace('true', 'true').replace('false', 'false').replace('nil', 'null')
    if not lua_str.startswith('{'): lua_str = '{' + lua_str + '}'
    try: return json.loads(lua_str)
    except: return {"error": "Lua parsing failed."}

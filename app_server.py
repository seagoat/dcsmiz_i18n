from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
import zipfile, os, io, mimetypes, shutil, re
from miz_lib import parse_lua_table, extract_usage_and_links, lua_to_dict

app = FastAPI()
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR): os.makedirs(UPLOAD_DIR)

def scan_all_files_for_keys(z):
    usage = {}
    for name in z.namelist():
        if name.startswith('l10n/') or name.endswith(('.ogg', '.wav', '.png', '.jpg', '.jpeg', '.bmp')): continue
        try:
            content = z.read(name).decode('utf-8', errors='ignore')
            keys = re.findall(r'(DictKey_[A-Za-z0-9_]+|ResKey_[A-Za-z0-9_]+)', content)
            for k in set(keys):
                if k not in usage: usage[k] = []
                usage[k].append(name)
        except: pass
    return usage

@app.get("/api/miz_files")
def list_miz_files():
    files = []
    for d in ['.', 'ref', UPLOAD_DIR]:
        if os.path.exists(d): files += [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.miz')]
    return sorted(list(set(files)))

@app.post("/api/upload")
async def upload_miz(file: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f: shutil.copyfileobj(file.file, f)
    return {"filename": file.filename, "path": path}

@app.get("/api/miz_data")
def get_miz_data(file_path: str):
    if not os.path.exists(file_path): raise HTTPException(status_code=404)
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            def_dict, def_res = {}, {}
            if "l10n/DEFAULT/dictionary" in z.namelist(): def_dict = parse_lua_table(z.read("l10n/DEFAULT/dictionary").decode('utf-8', errors='ignore'))
            if "l10n/DEFAULT/mapResource" in z.namelist(): def_res = parse_lua_table(z.read("l10n/DEFAULT/mapResource").decode('utf-8', errors='ignore'))
            
            mission_raw = z.read("mission").decode('utf-8', errors='ignore') if "mission" in z.namelist() else ""
            usage, links = extract_usage_and_links(mission_raw)
            mission_tree = lua_to_dict(mission_raw) if mission_raw else {}
            file_usage = scan_all_files_for_keys(z)

            languages = {}
            l10n_folders = {n.split('/')[1] for n in z.namelist() if n.startswith('l10n/') and len(n.split('/')) > 1}
            for lang in l10n_folders:
                c_d, c_r = {}, {}
                if f"l10n/{lang}/dictionary" in z.namelist(): c_d = parse_lua_table(z.read(f"l10n/{lang}/dictionary").decode('utf-8', errors='ignore'))
                if f"l10n/{lang}/mapResource" in z.namelist(): c_r = parse_lua_table(z.read(f"l10n/{lang}/mapResource").decode('utf-8', errors='ignore'))
                languages[lang] = {
                    "dictionary": {k: {"val": c_d.get(k, def_dict.get(k, "")), "is_fallback": k not in c_d} for k in (set(def_dict.keys())|set(c_d.keys()))},
                    "resources": {k: {"val": c_r.get(k, def_res.get(k, "")), "is_fallback": k not in c_r} for k in (set(def_res.keys())|set(c_r.keys()))}
                }
            return {"filename": os.path.basename(file_path), "path": file_path, "languages": languages, "links": links, "usage": usage, "file_usage": file_usage, "mission_tree": mission_tree}
    except Exception as e: raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resource")
def get_resource(file_path: str, lang: str, res_name: str):
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            for p in [f"l10n/{lang}/{res_name}", f"l10n/DEFAULT/{res_name}"]:
                if p in z.namelist(): return StreamingResponse(io.BytesIO(z.read(p)), media_type=mimetypes.guess_type(p)[0] or "application/octet-stream")
            raise HTTPException(status_code=404)
    except: raise HTTPException(status_code=500)

@app.get("/")
def read_index(): return FileResponse('index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

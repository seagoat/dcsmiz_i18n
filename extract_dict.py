import zipfile
import re
import json

def extract():
    z = zipfile.ZipFile('ref/R1 M01.miz', 'r')
    content = z.read('l10n/DEFAULT/dictionary').decode('utf-8')
    pattern = re.compile(r'\["(.*?)"\]\s*=\s*("(.*?)"|\[\[(.*?)\]\])\s*,', re.DOTALL)
    data = {}
    for match in pattern.finditer(content):
        key = match.group(1)
        value = match.group(3) if match.group(3) is not None else match.group(4)
        data[key] = value
    
    with open('r1_m01_en.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    extract()

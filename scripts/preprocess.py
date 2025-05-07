import json
from utils import extract_pinyin
    
with open("data/polyphones.json", "r", encoding="utf-8") as f:
    polyphones_idioms = json.load(f)

with open("data/polyphones_idioms.txt", "w", encoding="utf-8") as f:
    for key in polyphones_idioms:
        print(key, file=f)

with open("data/idioms.txt", "r", encoding="utf-8") as f:
    idioms = [line.strip() for line in f if line.strip()]

with open("data/polyphones_idioms.txt", "r", encoding="utf-8") as f:
    idioms += [line.strip() for line in f if line.strip()]

processed = []

for idiom in idioms:
    words, initials, finals, tones = extract_pinyin(idiom)
    processed.append({"word": idiom, "initials": initials, "finals": finals, "tones": tones})

with open("data/processed_idioms.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

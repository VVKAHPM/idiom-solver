import json
from utils import extract_pinyin
    


with open("data/idioms.txt", "r", encoding="utf-8") as f:
    idioms = [line.strip() for line in f if line.strip()]

processed = []

for idiom in idioms:
    initials, finals, tones = extract_pinyin(idiom)
    processed.append({"word": idiom, "initials": initials, "finals": finals, "tones": tones})

with open("data/processed_idioms.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

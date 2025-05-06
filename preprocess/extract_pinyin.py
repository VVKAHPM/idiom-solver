import json
from pypinyin import pinyin, Style

def extract_pinyin(word):
    initials = pinyin(word, style=Style.INITIALS, strict=False)
    finals = pinyin(word, style=Style.FINALS, strict=False)
    tones = pinyin(word, style=Style.TONE3)

    initial_list = []
    final_list = []
    tones_number = []

    initial_list = [x[0] for x in initials]
    final_list = [x[0] for x in finals]

    for tone in tones:
        syllable = tone[0]
        if syllable[-1].isdigit():
            tones_number.append(syllable[-1])
        else:
            tones_number.append(0)
    
    return initial_list, final_list, tones_number
    


with open("data/idiom.json", "r", encoding="utf-8") as f:
    idioms = json.load(f)

processed = []

for idiom in idioms:
    word = idiom["word"]
    initials, finals, tones = extract_pinyin(word)
    processed.append({"word": word, "initials": initials, "finals": finals, "tones": tones})

with open("data/processed_idioms.json", "w", encoding="utf-8") as f:
    json.dump(processed, f, ensure_ascii=False, indent=2)

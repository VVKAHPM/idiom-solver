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
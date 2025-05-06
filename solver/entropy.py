from scripts.utils import extract_pinyin

def judge_idiom(guess, result, idiom):
    words, initials, finals, tones = extract_pinyin(guess) 
    for i in range(0, 4):


def size_of_possible_idioms(condition, candidates):
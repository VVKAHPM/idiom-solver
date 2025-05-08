import math
# from tqdm import tqdm
from solver.feedback_parser import get_feedback
from scripts.utils import extract_pinyin 

INITIAL_TOP5 = [
    ("研经铸史", 12.963477340563239),
    ("积善余庆", 12.827873128560476),
    ("阳煦山立", 12.804475258254376),
    ("独具只眼", 12.74220261125653),
    ("身不由己", 12.722705815635168)
]

def feedback_to_key(feedback):
    return tuple(tuple(x) for x in feedback)

def calculate_entropy(guess, candidates, idiomdict=None):
    distribution = {}
    for candidate in candidates:
        feedback = get_feedback(candidate, guess, idiomdict)
        key = feedback_to_key(feedback)
        if key in distribution:
            distribution[key] += 1
        else:
            distribution[key] = 1

    result = 0.0
    candidate_size = len(candidates)
    for possible_result in distribution:
        prob = distribution[possible_result] / candidate_size
        result -= prob * math.log2(prob)

    return result

def rank_by_entropy(guesslist, candidates, topk=5, idiomdict=None, initialflag=False):
    if initialflag:
        return INITIAL_TOP5
    entropy_list = [
        (guess, calculate_entropy(guess, candidates, idiomdict))
        for guess in guesslist
    ]
    entropy_list.sort(key=lambda x: x[1] + 0.001 * (int)(x[0] in candidates), reverse=True)
    return entropy_list[:topk]

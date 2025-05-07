import math
from functools import lru_cache
from tqdm import tqdm
from solver.feedback_parser import get_feedback
from scripts.utils import extract_pinyin 

@lru_cache(maxsize=None)
def cached_feedback(answer, guess):
    return get_feedback(answer, guess)

def feedback_to_key(feedback):
    return tuple(tuple(x) for x in feedback)

def calculate_entropy(guess, candidates):
    distribution = {}
    for candidate in candidates:
        feedback = cached_feedback(candidate, guess)
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

def rank_by_entropy(candidates, topk=5):
    entropy_list = [
        (guess, calculate_entropy(guess, candidates))
        for guess in tqdm(candidates, desc="计算信息熵")
    ]
    entropy_list.sort(key=lambda x: x[1], reverse=True)
    return entropy_list[:topk]

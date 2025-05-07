import math
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from solver.feedback_parser import get_feedback
from scripts.utils import extract_pinyin  # 假设你有一个提取拼音的函数

# 缓存反馈结果
@lru_cache(maxsize=None)
def cached_feedback(answer, guess):
    return get_feedback(answer, guess)

# 将反馈转换为 key
def feedback_to_key(feedback):
    return tuple(tuple(x) for x in feedback)

# 计算信息熵
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

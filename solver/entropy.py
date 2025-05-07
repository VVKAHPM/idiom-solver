from solver.feedback_parser import get_feedback
import math

def feedback_to_key(feedback):
    return tuple(tuple(x) for x in feedback)

def calculate_entropy(guess, candidates):
    distribution = {}
    for candidate in candidates:
        feedback = get_feedback(candidate, guess)
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
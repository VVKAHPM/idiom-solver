from solver.feedback_parser import get_feedback

def prune(guess, result, candidates, idiomdict):
    new_candidates = []
    for candidate in candidates:
        if result == get_feedback(candidate, guess, idiomdict):
            new_candidates.append(candidate)
    return new_candidates
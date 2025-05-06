from scripts.utils import extract_pinyin

def compare(list1, list2):
    """
    :param list1: The answer
    :param list2: The guess
    """
    result = [2] * 4
    l1_used = [False] * 4  
    l2_used = [False] * 4  

    for i in range(4):
        if list1[i] == list2[i]:
            result[i] = 0
            l1_used[i] = True
            l2_used[i] = True

    for i in range(4):
        if not l2_used[i]:
            for j in range(4):
                if not l1_used[j] and list2[i] == list1[j]:
                    result[i] = 1
                    l1_used[j] = True
                    break

    return result

def get_feedback(answer, guess):
    return [compare(x, y) for x, y in zip(extract_pinyin(answer), extract_pinyin(guess))]

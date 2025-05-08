from scripts.utils import extract_pinyin

def compare(list1, list2):
    """
    :param list1: The answer
    :param list2: The guess
    """
    result = [-1] * 4
    l1_used = [False] * 4

    for i in range(4):
        if list2[i] == "":
            continue
        if list1[i] == list2[i]:
            result[i] = 0
            l1_used[i] = True

    for i in range(4):
        if result[i] == -1 and list2[i] != "":
            for j in range(4):
                if not l1_used[j] and list2[i] == list1[j]:
                    result[i] = 1
                    l1_used[j] = True
                    break
            if result[i] == -1:
                result[i] = 2

    return result

def get_feedback(answer, guess, idiomdict=None):
    if not idiomdict:
        return [compare(x, y) for x, y in zip(extract_pinyin(answer), extract_pinyin(guess))]
    else:
        return [compare(x, y) for x, y in zip(idiomdict[answer], idiomdict[guess])]

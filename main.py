import json
from solver.filter import prune

def get_user_feedback():
    dimensions = ["汉字", "声母", "韵母", "音调"]
    feedback = []

    for dim in dimensions:
        while True:
            user_input = input(f"请输入{dim}的反馈(四个数字，以空格分隔，如 0 2 1 2): ").strip().split()
            if len(user_input) != 4 or not all(x in {"0", "1", "2", "-1"} for x in user_input):
                print("输入格式不正确,请重新输入四个数字: ")
                continue
            feedback.append([int(x) for x in user_input])
            break

    return feedback

# with open("data/test_idioms.txt", "r", encoding="utf-8") as f:
#     candidates = [line.strip() for line in f if line.strip()]
with open("data/processed_idioms.json", "r", encoding="utf-8") as f:
    idioms = json.load(f)

candidates = [item["word"] for item in idioms]

while len(candidates) > 1:
    # top5 = rank_by_entropy(candidates)
    # print("信息熵最大的五个成语为:")
    # for word, entropy in top5:
    #     print(f"{word}: {entropy:.4f} bits")
    
    guess = input("请输入你的猜测: ")
    print("请输入你的猜测反馈: (-1, 空; 0: 位置正确; 1: 位置错误但存在; 2: 不存在)")
    result = get_user_feedback()
    candidates = prune(guess, result, candidates)
    print(f"还剩下 {len(candidates)} 个候选成语")
    print(candidates)

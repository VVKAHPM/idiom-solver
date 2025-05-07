import json
from solver.entropy import rank_by_entropy

with open("data/test_idioms.txt", "r", encoding="utf-8") as f:
    candidates = [line.strip() for line in f if line.strip()]
    
while len(candidates) > 1:
    top5 = rank_by_entropy(candidates)
    for word, entropy in top5:
        print(f"{word}: {entropy:.4f} bits")
    break
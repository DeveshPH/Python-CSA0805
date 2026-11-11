from time import perf_counter
from collections import Counter
import random

def count_repeated_scan(words):
    return {w: words.count(w) for w in set(words)}

def count_once(words):
    return dict(Counter(words))

def compare(n=100_000):
    random.seed(7)
    words = [f"w{random.randrange(1000)}" for _ in range(n)]
    for fn in (count_repeated_scan, count_once):
        start = perf_counter()
        result = fn(words)
        elapsed = perf_counter() - start
        print(fn.__name__, len(result), f"{elapsed:.6f}s")
    assert count_repeated_scan(words[:500]) == count_once(words[:500])

if __name__ == "__main__":
    compare()

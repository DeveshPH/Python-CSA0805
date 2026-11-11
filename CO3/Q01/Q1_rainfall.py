import random, time

def moving_naive(values, window=7):
    return [sum(values[i:i+window]) / window
            for i in range(len(values)-window+1)]

def moving_running(values, window=7):
    if len(values) < window:
        return []
    current = sum(values[:window])
    result = [current / window]
    for i in range(window, len(values)):
        current += values[i] - values[i-window]
        result.append(current / window)
    return result

if __name__ == "__main__":
    random.seed(10)
    for n in (365, 36_500, 365_000):
        x = [random.uniform(0, 50) for _ in range(n)]
        for fn in (moving_naive, moving_running):
            start=time.perf_counter(); out=fn(x); elapsed=time.perf_counter()-start
            print(n, fn.__name__, len(out), f"{elapsed:.6f}s")

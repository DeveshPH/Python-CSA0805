import time

def build_plus(parts):
    text = ""
    for part in parts:
        text += part + ";"
    return text

def build_join(parts):
    return ";".join(parts) + (";" if parts else "")

def benchmark():
    for n in (1_000, 10_000, 200_000):
        items = [f"Item{i}:Rs{i % 50}" for i in range(n)]
        results = []
        for fn in (build_plus, build_join):
            start = time.perf_counter()
            value = fn(items)
            results.append((fn.__name__, time.perf_counter() - start, len(value)))
        print(n, results, "same:", build_plus(items) == build_join(items))

if __name__ == "__main__":
    benchmark()

import re, time, random
calls = ["seeds not received seeds delayed", "fertiliser price high",
         "seeds price high subsidy not received"]
STOP = {"not", "high"}

def frequencies(texts, stop):
    counts = {}
    for text in texts:
        for word in re.findall(r"[a-z]+", text.lower()):
            if word not in stop:
                counts[word] = counts.get(word, 0) + 1
    return counts

def top(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]

if __name__ == "__main__":
    print(top(frequencies(calls, STOP), 3))

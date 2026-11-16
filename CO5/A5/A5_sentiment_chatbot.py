import re, sqlite3
POSITIVE = {"clean", "good", "safe", "improved", "fresh", "excellent"}
NEGATIVE = {"polluted", "bad", "smoke", "dust", "dangerous", "worse", "dirty"}
NEGATORS = {"not", "never", "no"}

def sentiment(text):
    words = re.findall(r"[a-z]+", text.lower())
    score = 0
    negate = False
    for word in words:
        if word in NEGATORS:
            negate = True
            continue
        if word in POSITIVE:
            score += -1 if negate else 1
            negate = False
        elif word in NEGATIVE:
            score += 1 if negate else -1
            negate = False
    return "positive" if score > 0 else "negative" if score < 0 else "neutral"

def summarise(text, k=2):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    tokens = [re.findall(r"[a-z]+", s.lower()) for s in sentences]
    stop = {"the","a","an","is","are","in","on","of","and","to","it","for"}
    freq = {}
    for words in tokens:
        for w in words:
            if w not in stop:
                freq[w] = freq.get(w, 0) + 1
    ranked = sorted(enumerate(sentences), key=lambda x: (
        -sum(freq.get(w,0) for w in tokens[x[0]]), x[0]))
    return [sentences[i] for i,_ in sorted(ranked[:k])]

def answer_pm25(question, con):
    match = re.search(r"pm\s*2\.?5.*?in\s+([a-z ]+?)(?:\s+today|\?|$)", question.lower())
    if not match:
        return "Please ask for PM2.5 in a named station."
    station = match.group(1).strip().title()
    row = con.execute("SELECT pm25 FROM readings WHERE station=? ORDER BY day DESC LIMIT 1",
                      (station,)).fetchone()
    return f"Latest PM2.5 at {station}: {row[0]}" if row else f"No reading found for {station}."

if __name__ == "__main__":
    print(sentiment("The air is not good today"))
    print(summarise("Smoke is heavy near school. PM2.5 is high. Smoke affects children.", 2))

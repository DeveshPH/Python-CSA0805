import re, sqlite3, time

POS={"clean","good","safe","fresh","improved","excellent"}
NEG={"polluted","bad","smoke","dust","dangerous","worse","dirty"}
NEGATE={"not","never","no"}

def score(text):
    words=re.findall(r"[a-z]+",text.lower())
    total=0; negate=False
    for w in words:
        if w in NEGATE: negate=True; continue
        if w in POS: total += -1 if negate else 1; negate=False
        elif w in NEG: total += 1 if negate else -1; negate=False
    return "positive" if total>0 else "negative" if total<0 else "neutral"

def extractive_summary(text,k=2):
    sentences=re.split(r"(?<=[.!?])\s+",text.strip())
    stop={"the","a","an","is","are","to","of","and","in","for"}
    counts={}
    words=[]
    for sentence in sentences:
        current=re.findall(r"[a-z]+",sentence.lower()); words.append(current)
        for w in current:
            if w not in stop: counts[w]=counts.get(w,0)+1
    ranked=sorted(range(len(sentences)),
                  key=lambda i:(-sum(counts.get(w,0) for w in words[i]),i))
    chosen=sorted(ranked[:k])
    return " ".join(sentences[i] for i in chosen)

def main():
    complaints=[
      "Smoke and dust are heavy near the school.",
      "The air is not good near the market.",
      "Air quality improved after rain.",
      "Children report a dangerous smell.",
      "The station reports clean air today."
    ] * 10
    labels=[score(c) for c in complaints]
    print("complaints:",len(complaints),"labels:",{x:labels.count(x) for x in set(labels)})
    sample="Smoke is heavy near school. PM2.5 is high. Smoke affects children."
    print("summary:",extractive_summary(sample))
    con=sqlite3.connect(":memory:")
    con.execute("CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL)")
    con.executemany("INSERT INTO readings VALUES(?,?,?)",
                    [("Adyar","2026-10-01",48),("Adyar","2026-10-02",55)])
    con.execute("CREATE INDEX idx_station_day ON readings(station,day)")
    start=time.perf_counter()
    print(con.execute("SELECT AVG(pm25) FROM readings WHERE station=? AND day>=?",
                      ("Adyar","2026-10-01")).fetchone())
    print("indexed query seconds:",time.perf_counter()-start)
    con.close()

if __name__=="__main__": main()

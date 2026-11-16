import csv, io, sqlite3, statistics
from datetime import datetime

RAW = """station,date,pm25,pm10,no2,temp,temp_unit
Adyar,2026-10-01,48,80,20,30,C
Adyar,2026-10-02,NA,75,18,31,C
Adyar,2026-10-03,,70,17,32,C
Guindy,2026-10-01,95,130,40,86,F
Guindy,2026-10-02,-5,120,38,87,F
Guindy,2026-10-03,121,140,44,88,F
Guindy,2026-10-04,1200,150,45,89,F
"""

def load_clean(text):
    rows, previous = [], {}
    reader = csv.DictReader(io.StringIO(text))
    required = {"station","date","pm25","pm10","no2","temp","temp_unit"}
    if not required.issubset(reader.fieldnames or []):
        raise ValueError("missing required CSV column")
    for raw in reader:
        try:
            station = raw["station"].strip().title()
            day = datetime.strptime(raw["date"], "%Y-%m-%d").date().isoformat()
            pm25_text = (raw["pm25"] or "").strip()
            if pm25_text.upper() in {"", "NA"}:
                continue
            pm25 = float(pm25_text)
            if not 0 <= pm25 <= 999:
                continue
            temp = float(raw["temp"])
            if raw["temp_unit"].strip().upper() == "F":
                temp = (temp - 32) * 5/9
            rows.append((station, day, pm25, float(raw["pm10"]), float(raw["no2"]), temp))
        except (ValueError, TypeError):
            continue
    return rows

def main():
    clean = load_clean(RAW)
    print("cleaned:", clean)
    con = sqlite3.connect(":memory:")
    con.execute("""CREATE TABLE readings(station TEXT, day TEXT, pm25 REAL,
                   pm10 REAL, no2 REAL, temp_c REAL, PRIMARY KEY(station,day))""")
    con.executemany("INSERT OR REPLACE INTO readings VALUES(?,?,?,?,?,?)", clean)
    print("station means:", con.execute(
        "SELECT station, AVG(pm25) FROM readings GROUP BY station").fetchall())
    print("Adyar October mean:", con.execute(
        "SELECT AVG(pm25) FROM readings WHERE station=? AND day BETWEEN ? AND ?",
        ("Adyar","2026-10-01","2026-10-31")).fetchone())
    print("daily:", con.execute(
        "SELECT station,day,MIN(pm25),MAX(pm25),AVG(pm25),COUNT(pm25) "
        "FROM readings GROUP BY station,day").fetchall())
    con.close()

if __name__ == "__main__":
    main()

# Package layout example:
# attendance/__init__.py, reader.py, stats.py, report.py
# reader.py
from pathlib import Path

def read_records(folder):
    for path in Path(folder).glob("*.csv"):
        with path.open(encoding="utf-8") as f:
            for line in f:
                yield path.name, line.rstrip("\n")

# stats.py
def percentage(present, total):
    return 0.0 if total == 0 else 100 * present / total

def three_day_absences(statuses):
    return any(statuses[i:i+3] == ["A", "A", "A"]
               for i in range(max(0, len(statuses)-2)))

# report.py
def write_report(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(",".join(map(str, row)) + "\n")

if __name__ == "__main__":
    print("Import the functions from attendance.reader, attendance.stats and attendance.report")

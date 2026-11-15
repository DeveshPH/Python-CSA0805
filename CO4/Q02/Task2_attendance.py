from pathlib import Path
from collections import defaultdict
import csv

def process_month(folder, report_path="attendance_report.csv", error_path="errors.csv"):
    counts = defaultdict(lambda: [0, 0])
    errors = []
    for file in sorted(Path(folder).glob("*.csv")):
        with file.open(encoding="utf-8", newline="") as handle:
            for line_no, line in enumerate(handle, 1):
                try:
                    reg, day, status = [x.strip() for x in line.strip().split(",")]
                    if status not in {"P", "A"}:
                        raise ValueError(f"invalid status {status!r}")
                    counts[reg][0] += 1
                    counts[reg][1] += status == "P"
                except ValueError as exc:
                    errors.append((file.name, line_no, line.strip(), str(exc)))
    with open(report_path, "w", newline="", encoding="utf-8") as out:
        writer=csv.writer(out); writer.writerow(["register","present","total","percent"])
        for reg,(total,present) in sorted(counts.items()):
            writer.writerow([reg,present,total,round(100*present/total,2)])
    with open(error_path, "w", newline="", encoding="utf-8") as out:
        writer=csv.writer(out); writer.writerow(["file","line","raw","error"]); writer.writerows(errors)
    return counts, errors

if __name__ == "__main__":
    print(process_month("daily_files"))

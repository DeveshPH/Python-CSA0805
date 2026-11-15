from pathlib import Path
import csv

def valid_email(email):
    if email.count("@") != 1:
        return False
    local, domain = email.split("@")
    return bool(local and "." in domain and not domain.startswith(".")
                and not domain.endswith(".") and " " not in email)

def process_registration_files(folder, output_folder="fest_output"):
    out = Path(output_folder); out.mkdir(parents=True, exist_ok=True)
    master, seen, errors, events = {}, set(), [], {}
    for path in sorted(Path(folder).glob("*.txt")):
        try:
            with path.open(encoding="utf-8") as handle:
                for line_no, line in enumerate(handle, 1):
                    try:
                        fields = [x.strip() for x in line.rstrip("\n").split(",")]
                        if len(fields) != 5:
                            raise ValueError("expected 5 comma-separated fields")
                        reg, name, dept, email, event_text = fields
                        if not valid_email(email):
                            raise ValueError("invalid email")
                        if reg in seen:
                            errors.append((path.name,line_no,"duplicate registration",reg)); continue
                        seen.add(reg)
                        record=(reg,name,dept,email,event_text)
                        master[reg]=record
                        for event in [x.strip() for x in event_text.split(";") if x.strip()]:
                            events.setdefault(event, []).append(record)
                    except ValueError as exc:
                        errors.append((path.name,line_no,str(exc),line.rstrip("\n")))
        except OSError as exc:
            errors.append((path.name,0,type(exc).__name__,str(exc)))
    with (out/"master.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["reg","name","dept","email","events"]); w.writerows(master.values())
    for event, records in events.items():
        with (out/f"{event.replace(' ','_')}.csv").open("w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["reg","name","dept","email"]); w.writerows(r[:4] for r in records)
    with (out/"errors.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["file","line","error","detail"]); w.writerows(errors)
    return master, events, errors

if __name__ == "__main__":
    print(process_registration_files("department_files"))

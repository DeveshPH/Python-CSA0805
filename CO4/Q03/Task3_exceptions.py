import os, tempfile

class InvalidRecord(Exception):
    """Attendance record does not match the required format."""

def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    reg, day, status = parts
    if status not in {"P", "A"}:
        raise InvalidRecord(f"invalid status {status!r}")
    return reg, day, status

def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, encoding="utf-8") as handle:
            for number, line in enumerate(handle, 1):
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as exc:
                    errors.append((number, str(exc)))
                    continue
                if status == "P": present += 1
                else: absent += 1
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"attendance file not found: {path}") from exc
    return present, absent, errors

if __name__ == "__main__":
    data=("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
          "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
        tmp.write(data)
    try: print(summarise(tmp.name))
    finally: os.remove(tmp.name)

def normalise(text):
    return text.strip().replace(" ", "").replace("-", "").upper()

def is_valid(reg):
    if len(reg) not in (9, 10):
        return False
    series_end = len(reg) - 4
    return (reg[:2].isalpha() and reg[2:4].isdigit()
            and reg[4:series_end].isalpha()
            and len(reg[4:series_end]) in (1, 2)
            and reg[series_end:].isdigit())

def format_receipt(reg):
    if not is_valid(reg):
        raise ValueError("Invalid registration number")
    return f"{reg[:2]} {reg[2:4]} {reg[4:-4]} {reg[-4:]}"

if __name__ == "__main__":
    samples = ["tn 09 ab 1234", "KA-01-M-0007", "TN9AB1234", "TN 22 1234 AB"]
    for raw in samples:
        value = normalise(raw)
        print(raw, "->", value, "valid" if is_valid(value) else "INVALID")

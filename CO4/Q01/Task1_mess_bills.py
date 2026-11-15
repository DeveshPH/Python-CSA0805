from decimal import Decimal, InvalidOperation
from pathlib import Path

def total_mess_bills(filename):
    total = Decimal("0.00")
    report, rejected = [], []
    with open(filename, "r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                reg, name, amount_text = [part.strip() for part in line.rstrip("\n").split(",")]
                amount = Decimal(amount_text)
                if not amount.is_finite() or amount < 0:
                    raise ValueError("amount must be a non-negative finite number")
                total += amount
                report.append(f"{reg} {name} {amount:.2f}")
            except (ValueError, InvalidOperation) as exc:
                rejected.append((line_no, line.rstrip("\n"), str(exc)))
    return total, report, rejected

if __name__ == "__main__":
    path = Path("mess_oct.txt")
    print(total_mess_bills(path))

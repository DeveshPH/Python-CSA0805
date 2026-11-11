from decimal import Decimal
from time import perf_counter

PAYMENT_TEXT = "33.40"

def measure(count):
    values = [PAYMENT_TEXT] * count
    start = perf_counter()
    float_total = sum(float(x) for x in values)
    float_seconds = perf_counter() - start
    start = perf_counter()
    decimal_total = sum((Decimal(x) for x in values), Decimal("0.00"))
    decimal_seconds = perf_counter() - start
    difference = Decimal(str(float_total)) - decimal_total
    print(f"n={count:>6} float={float_total:.12f} Decimal={decimal_total} diff={difference} "
          f"float_s={float_seconds:.6f} decimal_s={decimal_seconds:.6f}")

for size in (300, 6000, 150000):
    measure(size)

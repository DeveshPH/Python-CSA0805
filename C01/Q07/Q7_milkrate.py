from decimal import Decimal, ROUND_HALF_UP

"""Rate card and payment functions for the village milk co-operative."""
BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")
STEP = Decimal("0.1")

def rate_per_litre(fat, snf):
    """Return the rate per litre rounded to two decimal places."""
    fat_steps = ((Decimal(str(fat)) - Decimal("3.5")) / STEP).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    snf_steps = ((Decimal(str(snf)) - Decimal("8.5")) / STEP).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def payout(litres, fat, snf):
    """Return the amount payable, rounded to two decimal places."""
    return (Decimal(str(litres)) * rate_per_litre(fat, snf)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    for litres, fat, snf in [(10, 3.5, 8.5), (8.5, 4.2, 8.7), (12, 3.1, 8.3)]:
        rate = rate_per_litre(fat, snf)
        pay = payout(litres, fat, snf)
        print(f"{litres:5} L fat {fat} snf {snf} rate {rate:6.2f} pay {pay:8.2f}")

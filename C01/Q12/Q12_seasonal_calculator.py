from decimal import Decimal, ROUND_HALF_UP

STEP = Decimal("0.1")
REFERENCE_FAT = Decimal("3.5")
REFERENCE_SNF = Decimal("8.5")
BONUS_THRESHOLD = Decimal("500")
BONUS_PER_LITRE = Decimal("0.50")
CENT = Decimal("0.01")

RATE_CARDS = {
    "regular": {"base": Decimal("30.00"), "fat_step": Decimal("0.40"), "snf_step": Decimal("0.30")},
    "april_june": {"base": Decimal("32.00"), "fat_step": Decimal("0.45"), "snf_step": Decimal("0.30")},
}

def rounded_steps(reading, reference):
    return ((reading - reference) / STEP).quantize(Decimal("1"), rounding=ROUND_HALF_UP)

def rate_per_litre(fat, snf, season="regular"):
    card = RATE_CARDS[season]
    fat_steps = rounded_steps(fat, REFERENCE_FAT)
    snf_steps = rounded_steps(snf, REFERENCE_SNF)
    return (card["base"] + fat_steps * card["fat_step"] + snf_steps * card["snf_step"]).quantize(CENT, rounding=ROUND_HALF_UP)

def ten_day_payment(total_litres, fat, snf, season="regular"):
    rate = rate_per_litre(fat, snf, season)
    base_payment = total_litres * rate
    bonus = total_litres * BONUS_PER_LITRE if total_litres > BONUS_THRESHOLD else Decimal("0.00")
    return (base_payment + bonus).quantize(CENT, rounding=ROUND_HALF_UP)

if __name__ == "__main__":
    fat, snf = Decimal("3.57"), Decimal("8.54")
    for season in ("regular", "april_june"):
        print(season, "rate=", rate_per_litre(fat, snf, season))
    print("500 L total=", ten_day_payment(Decimal("500"), fat, snf, "april_june"))
    print("501 L total=", ten_day_payment(Decimal("501"), fat, snf, "april_june"))

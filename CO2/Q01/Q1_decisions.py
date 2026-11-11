def subsidy(units, ration_card, age_over_80):
    if units <= 100:
        return "full subsidy"
    elif 101 <= units <= 200 and ration_card:
        return "partial subsidy"
    elif units > 200 and age_over_80:
        return "senior-citizen exception"
    return "no subsidy"

cases = [(100, False, False), (101, True, False), (200, True, False),
         (201, False, True), (201, False, False), (100, True, True),
         (150, False, True), (200, True, True)]
for case in cases:
    print(case, "->", subsidy(*case))

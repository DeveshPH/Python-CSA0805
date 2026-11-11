CORRECT_OTP = "482913"

def verify_while():
    attempts = 0
    while attempts < 3:
        entered = input("OTP: ").strip()
        if not entered:
            print("Blank entry; it does not count.")
            continue
        attempts += 1
        if entered == CORRECT_OTP:
            print("Verified")
            break
        print("Incorrect")
    else:
        print("Account locked for 30 minutes")

def verify_for():
    for attempt in range(3):
        # Inner loop obtains one non-blank attempt; blank entries do not use a turn.
        while True:
            entered = input("OTP: ").strip()
            if entered:
                break
            print("Blank entry; it does not count.")
        if entered == CORRECT_OTP:
            print("Verified")
            break
        print("Incorrect")
    else:
        print("Account locked for 30 minutes")

if __name__ == "__main__":
    verify_while()

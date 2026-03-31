def read_positive_amount(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            amount = float(raw)
        except ValueError:
            print(f"  '{raw}' is not a valid number. Please try again.")
            continue

        if amount <= 0:
            print("  Amount must be greater than zero. Please try again.")
            continue

        return amount


def read_non_negative_amount(prompt: str) -> float:
    while True:
        raw = input(prompt).strip()
        try:
            amount = float(raw)
        except ValueError:
            print(f"  '{raw}' is not a valid number. Please try again.")
            continue

        if amount < 0:
            print("  Value cannot be negative. Please try again.")
            continue

        return amount


def read_non_empty_string(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  This field cannot be empty. Please enter a value.")

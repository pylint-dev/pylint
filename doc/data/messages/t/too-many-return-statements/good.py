NUMBERS_TO_STRINGS = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
}


def to_string(x):
    return f"This is {NUMBERS_TO_STRINGS.get(x)}."

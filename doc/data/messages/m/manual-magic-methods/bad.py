three = 3.0.__str__()  # [manual-magic-methods]
twelve = "1".__add__("2")  # [manual-magic-methods]


def is_bigger_than_two(x):
    return x.__gt__(2)  # [manual-magic-methods]

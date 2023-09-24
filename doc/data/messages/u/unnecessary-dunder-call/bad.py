three = (3.0).__str__()  # [unnecessary-dunder-call]
twelve = "1".__add__("2")  # [unnecessary-dunder-call]


def is_bigger_than_two(x):
    return x.__gt__(2)  # [unnecessary-dunder-call]

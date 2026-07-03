from .bad import count_to_one  # [cyclic-import]


def count_to_two():
    return count_to_one() + 1

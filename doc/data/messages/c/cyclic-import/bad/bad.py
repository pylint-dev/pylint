def count_to_one():
    return 1


def count_to_three():
    from .bad2 import count_to_two  # another cyclic-import

    return count_to_two() + 1

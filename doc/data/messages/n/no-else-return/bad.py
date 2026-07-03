def compare_numbers(a: int, b: int) -> int:
    if a == b:  # [no-else-return]
        return 0
    elif a < b:
        return -1
    else:
        return 1

def find_even_number(lst):
    for x in lst:
        if x % 2 == 0:
            break

    return x  # [undefined-loop-variable]

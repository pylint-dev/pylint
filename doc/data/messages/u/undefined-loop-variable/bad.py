def find_even_number(numbers):
    for x in numbers:
        if x % 2 == 0:
            break
    return x  # [undefined-loop-variable]

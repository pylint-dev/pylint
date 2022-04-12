def even_number_under(n: int):
    for i in range(n):
        if i%2 == 1:  # [no-else-continue]
            continue
        yield i

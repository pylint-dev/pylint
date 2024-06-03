def bad_yield_from(generator):
    for item in generator:  # [use-yield-from]
        yield item

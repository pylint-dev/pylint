def bad_yield_from(generator):
    for item in generator:
        yield item

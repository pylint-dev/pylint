def iterator_prefix(iterator, stop: int):
    for i, item in enumerate(iterator):
        if i == stop:
            break
        yield item

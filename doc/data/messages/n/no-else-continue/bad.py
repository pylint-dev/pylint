def iterator_suffix(iterator, stop: int):
    for i, item in enumerate(iterator):
        if i < stop:  # [no-else-continue]
            continue
        else:
            yield item

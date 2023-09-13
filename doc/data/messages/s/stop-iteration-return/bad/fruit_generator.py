def fruit_generator():
    for fruit in ["apple", "banana"]:
        yield fruit
    raise StopIteration  # [stop-iteration-return]

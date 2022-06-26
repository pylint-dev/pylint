def div(x, y):
    try:
        return x / y
    except ZeroDivisionError:
        raise None  # [raising-bad-type]

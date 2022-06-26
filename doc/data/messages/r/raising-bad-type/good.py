def div(x, y):
    try:
        return x / y
    except ZeroDivisionError as e:
        raise ValueError from e

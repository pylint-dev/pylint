try:
    1 / 0
except ZeroDivisionError as e:
    raise ValueError from e

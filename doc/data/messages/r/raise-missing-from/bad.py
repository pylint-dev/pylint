try:
    1 / 0
except ZeroDivisionError as e:
    raise ValueError("Rectangle Area cannot be zero")  # [raise-missing-from]

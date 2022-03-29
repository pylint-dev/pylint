def divide(x, y):
    result = 0
    try:
        result = x / y
    except ZeroDivisionError as exc:
        raise ValueError(f"Division by zero when dividing {x} by {y} !") from exc
    return result

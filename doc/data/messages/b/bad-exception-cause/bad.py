def divide(x, y):
    result = 0
    try:
        result = x / y
    except ZeroDivisionError:
        raise ValueError(f"Division by zero when dividing {x} by {y} !") from result  # [bad-exception-cause]
    return result

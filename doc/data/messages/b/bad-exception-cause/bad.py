def divide(x, y):
    result = 0
    try:
        result = x / y
    except ZeroDivisionError:
        # +1: [bad-exception-cause]
        raise ValueError(f"Division by zero when dividing {x} by {y} !") from result
    return result

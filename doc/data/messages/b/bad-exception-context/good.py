def divide(x, y):
    result = 0
    try:
        result = x / y
    except ZeroDivisionError as exc:
        raise Exception("Can't divide by zero!") from exc
    return result

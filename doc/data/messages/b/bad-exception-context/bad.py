def divide(x, y):
    result = 0
    try:
        result = x / y
    except ZeroDivisionError:
        raise Exception("Can't divide by zero!") from result  # [bad-exception-context]
    return result

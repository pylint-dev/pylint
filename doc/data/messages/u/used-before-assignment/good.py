def divide_by_zero(x):
    try:
        res = x / 0
        return res
    except ZeroDivisionError as e:
        print(e)

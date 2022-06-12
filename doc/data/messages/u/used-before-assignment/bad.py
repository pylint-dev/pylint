def divide_by_zero(x):
    try:
        res = x / 0
    except ZeroDivisionError as e:
        pass
    finally:
        return res  # [used-before-assignment]

    print(e)  # [used-before-assignment]

import random


def divide_by_random_int(x):
    try:
        res = x / random.randint(0, 2)
    except ZeroDivisionError as e:
        pass
    finally:
        print(res)  # [used-before-assignment]

    print(e)  # [used-before-assignment]

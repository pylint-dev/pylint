import random


def divide_by_random_int(x):
    try:
        res = x / random.randint(0, 2)
        print(res)
    except ZeroDivisionError as e:
        print(e)

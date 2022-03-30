# pylint: disable=missing-docstring,invalid-name
def main1():
    try:
        raise ValueError
    except ValueError as e:  # [unused-variable]
        pass

    print(e)  # [used-before-assignment]


def main2():
    try:
        raise ValueError
    except ValueError as e:
        print(e)


def main3():
    try:
        raise ValueError
    except ValueError as e:  # [unused-variable]
        pass

    e = 10
    print(e)


def main4():
    try:
        raise ValueError
    except ValueError as e:  # [unused-variable]
        pass

    try:
        raise ValueError
    except ValueError as e:
        pass

    try:
        raise ValueError
    except ValueError as e:
        pass

    print(e)  # [used-before-assignment]


def main5():
    try:
        print([e for e in range(3) if e])
    except ValueError as e:
        print(e)

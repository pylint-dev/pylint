"""Check for else branches on loops with break and return only."""


def test_return_for():
    """else + return is not acceptable."""
    for i in range(10):
        if i % 2:
            return i
    else:
        print('math is broken')  # [useless-else-on-loop]
    return None

def test_return_while():
    """else + return is not acceptable."""
    while True:
        return 1
    else:
        print('math is broken')  # [useless-else-on-loop]
    return None


while True:
    def short_fun():
        """A function with a loop."""
        for _ in range(10):
            break
else:
    print('or else!')  # [useless-else-on-loop]


while True:
    while False:
        break
else:
    print('or else!')  # [useless-else-on-loop]

for j in range(10):
    pass
else:
    print('fat chance')  # [useless-else-on-loop]
    for j in range(10):
        break


def test_return_for2():
    """no false positive for break in else

    https://bitbucket.org/logilab/pylint/issue/117/useless-else-on-loop-false-positives
    """
    for i in range(10):
        for _ in range(i):
            if i % 2:
                break
        else:
            break
    else:
        print('great math')


def test_break_in_orelse_deep():
    """no false positive for break in else deeply nested
    """
    for _ in range(10):
        if 1 < 2:  # pylint: disable=comparison-of-constants
            for _ in range(3):
                if 3 < 2:  # pylint: disable=comparison-of-constants
                    break
            else:
                break
    else:
        return True
    return False


def test_break_in_orelse_deep2():
    """should rise a useless-else-on-loop message, as the break statement is only
    for the inner for loop
    """
    for _ in range(10):
        if 1 < 2:  # pylint: disable=comparison-of-constants
            for _ in range(3):
                if 3 < 2:  # pylint: disable=comparison-of-constants
                    break
            else:
                print("all right")
    else:
        return True  # [useless-else-on-loop]
    return False


def test_break_in_orelse_deep3():
    """no false positive for break deeply nested in else
    """
    for _ in range(10):
        for _ in range(3):
            pass
        else:
            if 1 < 2:  # pylint: disable=comparison-of-constants
                break
    else:
        return True
    return False

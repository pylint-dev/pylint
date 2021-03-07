# pylint: disable=missing-docstring,no-else-return,using-constant-test
def get_list():
    return [1] if True else [2]


def find_int():
    return int(get_list()[0])


def func():
    if True:
        return find_int()
    else:
        return find_int()


def test():
    resp = func()
    assert resp / resp > 0
    return resp

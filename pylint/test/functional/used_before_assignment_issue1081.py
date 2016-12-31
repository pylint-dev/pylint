# pylint: disable=missing-docstring,invalid-name,redefined-outer-name

x = 24


def used_before_assignment_1(a):
    if x == a:  # [used-before-assignment]
        for x in [1, 2]:
            pass


def used_before_assignment_2(a):
    if x == a:  # [used-before-assignment]
        pass
    x = 2


def used_before_assignment_3(a):
    if x == a:  # [used-before-assignment]
        if x > 3:
            x = 2


def not_used_before_assignment(a):
    if x == a:
        pass


def not_used_before_assignment_2(a):
    x = 3
    if x == a:
        pass

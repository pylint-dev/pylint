# pylint: disable=missing-docstring,invalid-name,too-few-public-methods

class Point2D:
    __match_args__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y


# Don't emit false-positive 'unused-variable' and 'undefined-varibable'
var = 42
match var:
    case [*rest1]:
        print(rest1)
    case {**rest2}:
        print(rest2)
    case Point2D(0, a):
        print(a)
    case Point2D(x=0, y=b) as new_point:
        print(b)
        print(new_point)
    case new_var:
        print(new_var)

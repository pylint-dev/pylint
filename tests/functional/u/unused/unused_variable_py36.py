# pylint: disable=missing-docstring

def function():
    ann: int = 0
    assign = 0

    def inner():
        nonlocal ann, assign
        ann += 1
        assign += 1
        return ann + assign

    return inner()

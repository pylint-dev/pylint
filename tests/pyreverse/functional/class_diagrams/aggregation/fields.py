# Test for https://github.com/pylint-dev/pylint/issues/9045

class P:
    pass

class A:
    x: P  # just type hint, no ownership, soassociation

class B:
    def __init__(self, x: P):
        self.x = x  # not instantiated, so aggregation

class C:
    x: P

    def __init__(self, x: P):
        self.x = x  # not instantiated, so aggregation

class D:
    x: P

    def __init__(self):
        self.x = P()  # instantiated, so composition

class E:
    def __init__(self):
        self.x = P()  # instantiated, so composition

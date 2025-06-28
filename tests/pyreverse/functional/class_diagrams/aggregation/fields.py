# Test for https://github.com/pylint-dev/pylint/issues/9045

class P:
    pass

class A:
    x: P  # just type hint, no ownership → Association

class B:
    def __init__(self, x: P):
        self.x = x  # receives object, not created → Aggregation

class C:
    x: P
    def __init__(self, x: P):
        self.x = x  # receives object, not created → Aggregation

class D:
    x: P
    def __init__(self):
        self.x = P()  # creates object → Composition

class E:
    def __init__(self):
        self.x = P()  # creates object → Composition

# Test for https://github.com/pylint-dev/pylint/issues/9045

class P:
    pass

class Association:
    x: P  # just type hint, no ownership → Association

class Aggregation1:
    def __init__(self, x: P):
        self.x = x  # receives object, not created → Aggregation

class Aggregation2:
    x: P
    def __init__(self, x: P):
        self.x = x  # receives object, not created → Aggregation

class Composition1:
    x: P
    def __init__(self):
        self.x = P()  # creates object → Composition

class Composition2:
    def __init__(self):
        self.x = P()  # creates object → Composition

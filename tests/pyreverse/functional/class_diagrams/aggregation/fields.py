# Test for https://github.com/pylint-dev/pylint/issues/9045

class P:
    pass

class A:
    x: P

class B:
    def __init__(self, x: P):
        self.x = x

class C:
    x: P

    def __init__(self, x: P):
        self.x = x

class D:
    x: P

    def __init__(self):
        self.x = P()

class E:
    def __init__(self):
        self.x = P()

# Test for https://github.com/pylint-dev/pylint/issues/10373

class P:
    pass

class A:
    x: P = P()

class B:
    __x: P = P()

# Test for https://github.com/pylint-dev/pylint/issues/9267
class A:
    def __init__(self) -> None:
        self.var = 2

class B:
    def __init__(self) -> None:
        self.a_obj = A()

    def func(self):
        self.a_obj = A()
        self.a_obj = A()

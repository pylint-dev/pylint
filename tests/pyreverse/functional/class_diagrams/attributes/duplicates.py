# Test for https://github.com/pylint-dev/pylint/issues/8189
class DuplicateFields():
    example1: int
    example2: int

    def __init__(self):
        self.example1 = 1
        self.example2 = 2


# Test for https://github.com/pylint-dev/pylint/issues/8522
class A:
    pass

class DuplicateArrows:
    a: A

    def __init__(self):
        self.a = A()



# Test for https://github.com/pylint-dev/pylint/issues/8888
class DuplicateAnnotations:
    def __init__(self) -> None:
        self.val: str | int = "1"
        self.lav: list[str] = []

    def bar(self) -> None:
        self.val = "2"
        self.lav = []

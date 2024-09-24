# pylint: disable = import-error, missing-module-docstring, missing-function-docstring, missing-class-docstring, too-few-public-methods,

from mod import A  # [unguarded-typing-import]
from mod import B

def f(_: A):
    pass

def g(x: B):
    assert isinstance(x, B)

class C:
    pass

class D:
    c: C

    def h(self):
        # --> BUG <--
        # pylint: disable = undefined-variable
        return [C() for _ in self.c]

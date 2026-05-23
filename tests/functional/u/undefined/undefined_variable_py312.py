# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,too-few-public-methods
# pylint: disable=unused-argument

def f[T](a: T) -> T:
    print(a)

class SomeClass[T, *Ts, **P]:
    def __init__(self, value: T):
        self.value = value


class Parent[T]:
    def __init__(self, x: T, y: S) -> None:  # [undefined-variable]
        ...

class Child[T](Parent[T, S]):  # [undefined-variable]
    ...

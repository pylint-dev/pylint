# pylint: disable=missing-function-docstring,missing-module-docstring,missing-class-docstring,too-few-public-methods

def f[T](a: T) -> T:
    print(a)

class ChildClass[T, *Ts, **P]:
    ...

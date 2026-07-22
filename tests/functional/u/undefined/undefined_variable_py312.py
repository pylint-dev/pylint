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


# Regression test for https://github.com/pylint-dev/pylint/issues/11058
# The type parameter is scoped to the alias; using it afterwards is a
# NameError at runtime (and used to crash the refactoring checker).
type AliasWithParam[U] = U | None
_ = U()  # [undefined-variable]

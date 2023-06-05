# pylint: disable=missing-function-docstring, missing-module-docstring, missing-class-docstring, expression-not-assigned, invalid-name
from dataclasses import dataclass, replace


def func_that_returns_something():
    return 1


func_that_returns_something()  # [function-return-not-assigned]

_ = func_that_returns_something()

if func_that_returns_something():
    pass


def func_that_returns_none():
    return None


def func_with_no_explicit_return():
    print("I am doing something")


func_that_returns_none()
func_with_no_explicit_return()

some_var = ""
# next line should probably raise?
func_that_returns_something() if some_var else func_that_returns_none()
_ = func_that_returns_something() if some_var else func_that_returns_none()
func_with_no_explicit_return() if some_var else func_that_returns_none()


@dataclass
class TestClass:
    value: int

    def return_self(self):
        return self

    def return_none(self):
        pass


inst = TestClass(1)
inst.return_self()  # [function-return-not-assigned]
inst.return_none()

replace(inst, value=3)  # [function-return-not-assigned]

inst = replace(inst, value=3)

inst.return_self()  # [function-return-not-assigned]
inst.return_none()
inst = inst.return_self()

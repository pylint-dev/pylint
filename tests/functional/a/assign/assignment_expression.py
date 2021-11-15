"""Test assignment expressions"""
# pylint: disable=missing-docstring,unused-argument,unused-import,invalid-name
# pylint: disable=blacklisted-name,unused-variable,pointless-statement,unused-variable
import re

if (a := True):
    x = a
else:
    x = False

x = b if (b := True) else False
x2: bool = b2 if (b2 := True) else False
x3 = 0
x3 += b3 if (b3 := 4) else 6

a = ["a   ", "b   ", "c   "]
c = [text for el in a if (text := el.strip()) == "b"]


# check wrong usage
assert err_a, (err_a := 2)  # [used-before-assignment]
print(err_b and (err_b := 2))  # [used-before-assignment]
values = (
    err_c := err_d,  # [used-before-assignment]
    err_d := 2,
)


# https://github.com/PyCQA/pylint/issues/3347
s = 'foo' if (fval := lambda: 1) is None else fval


# https://github.com/PyCQA/pylint/issues/3953
assert (n := 2) == 1, f"Expected 1, but got {n}"
dict({1: (o := 2)}, data=o)
assert (p := 2) == 1, \
    p

FOO_PATT = re.compile("")
foo = m.group("foo") if (m := FOO_PATT.match("")) else False


# https://github.com/PyCQA/pylint/issues/3865
if (c := lambda: 2) and c():
    print("ok")

def func():
    print((d := lambda: 2) and d)


# https://github.com/PyCQA/pylint/issues/3275
values = (
    e := 1,
    f := e,
)
print(values)

function = lambda: (
    h := 1,
    i := h,
)
print(function())


# https://github.com/PyCQA/pylint/issues/3763
foo if (foo := 3 - 2) > 0 else 0


# https://github.com/PyCQA/pylint/issues/4238
l1 = f'The number {(count1 := 4)} ' \
     f'is equal to {count1}'
l2: str = (
    f'The number {(count2 := 4)} '
    f'is equal to {count2}'
)
l3 = "Hello "
l3 += (
    f'The number {(count3 := 4)} '
    f'is equal to {count3}'
)


# https://github.com/PyCQA/pylint/issues/4301
def func2():
    return f'The number {(count := 4)} ' \
           f'is equal to {count}'


# https://github.com/PyCQA/pylint/issues/4828
def func3():
    return bar if (bar := "") else ""


# Lambda and IfExp
def func4():
    l = lambda x: y if (y := x) else None


# Crash related to assignment expression in nested if statements
# See https://github.com/PyCQA/pylint/issues/5178
def func5(val):
    variable = None

    if val == 1:
        variable = "value"
        if variable := "value":
            pass

    elif val == 2:
        variable = "value_two"
        variable = "value_two"

    return variable

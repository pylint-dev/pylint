"""Test assignment expressions"""
# pylint: disable=missing-docstring,unused-argument,unused-import,invalid-name,blacklisted-name,unused-variable
import re

if (a := True):
    x = a
else:
    x = False

x = b if (b := True) else False

a = ["a   ", "b   ", "c   "]
c = [text for el in a if (text := el.strip()) == "b"]


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


# check wrong usage
assert err_a, (err_a := 2)  # [used-before-assignment]
print(err_b and (err_b := 2))  # [used-before-assignment]
values = (
    err_c := err_d,  # [used-before-assignment]
    err_d := 2,
)

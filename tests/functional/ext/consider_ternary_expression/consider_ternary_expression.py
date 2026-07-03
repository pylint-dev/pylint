# pylint: disable=invalid-name, undefined-variable, unused-variable, missing-function-docstring, missing-module-docstring
# pylint: disable=unsupported-assignment-operation, line-too-long

if f():  # [consider-ternary-expression]
    x = 4
else:
    x = 5

if g():
    y = 3
elif h():
    y = 4
else:
    y = 5

def a():
    if i():  # [consider-ternary-expression]
        z = 4
    else:
        z = 5

if f():
    x = 4
    print(x)
else:
    x = 5

if f():
    x[0] = 4
else:
    x = 5

if f():
    x = 4
else:
    y = 5

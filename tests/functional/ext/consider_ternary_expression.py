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

def foo(x, y, z):
    # Maximum number of boolean expressions in an if statement (by default 5)
    if (x and y and z) and (x % 2 == 0 and y % 2 == 0 and z % 2 == 0):  # [too-many-boolean-expressions]
        pass

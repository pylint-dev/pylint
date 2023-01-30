def can_be_divided_by_two_and_are_not_zero(x, y, z):
    # Maximum number of boolean expressions in an if statement (by default 5)
    # +1: [too-many-boolean-expressions]
    if (x and y and z) and (x % 2 == 0 and y % 2 == 0 and z % 2 == 0):
        pass

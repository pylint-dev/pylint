def can_be_divided_by_two_and_are_not_zero(x, y, z):
    if all(i and i % 2 == 0 for i in [x, y, z]):
        pass

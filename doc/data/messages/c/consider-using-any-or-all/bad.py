def any_even(items):
    """Return True if the list contains any even numbers"""
    for item in items:  # [consider-using-any-or-all]
        if item % 2 == 0:
            return True
    return False


def all_even(items):
    """Return True if the list contains all even numbers"""
    for item in items:  # [consider-using-any-or-all]
        if not item % 2 == 0:
            return False
    return True

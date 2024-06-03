def all_even(items):
    """Return True if the list contains all even numbers"""
    return all(item % 2 == 0 for item in items)

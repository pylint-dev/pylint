def any_even(items):
    """Return True if the list contains any even numbers"""
    return any(item % 2 == 0 for item in items)

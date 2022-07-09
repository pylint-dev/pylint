
def any_even(items):
    """Return True if the list contains any even numbers"""
    return any(item % 2 == 0 for item in items)

def all_even(items):
    """Return True if the list contains all even numbers"""
    return all(item % 2 == 0 for item in items)

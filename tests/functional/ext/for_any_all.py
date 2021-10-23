"""Functional test"""

def any_even(items):
    """Return True if the list contains any even numbers"""
    for item in items: # [consider-using-any-all]
        if item % 2 == 0:
            return True
    return False

def is_from_string(item):
    """Return True if one of parents of item is a string"""
    for parent in item.parents(): # [consider-using-any-all]
        if isinstance(parent, str):
            return True
    return False

def nested_check(items):
    """Tests that for loops at deeper levels are picked up"""
    if items and len(items) > 5:
        print(items)
        for item in items: # [consider-using-any-all]
            if item in (1, 2, 3):
                return False
        return True
    print(items)
    return items[3] > 5

def suppress_long_suggestion(items):
    """Tests that we get generic message if the suggestion would be long"""
    if items and len(items) > 5:
        print(items)
        for item in items: # [consider-using-any-all]
            if (item in (1, 2, 3)
                or item.get_next_prime() > item + 150
                or item.get_next_passing_without_skipping_nulls()
                or item * 300 > 15000
                and str(item) not in ("120000000", "150000000")):
                return False
        return True
    print(items)
    return items[3] > 5

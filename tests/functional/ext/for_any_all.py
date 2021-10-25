"""Functional test"""

def any_even(items):
    """Return True if the list contains any even numbers"""
    for item in items: # [consider-using-any-or-all]
        if item % 2 == 0:
            return True
    return False

def all_even(items):
    """Return True if the list contains all even numbers"""
    for item in items: # [consider-using-any-or-all]
        if not item % 2 == 0:
            return False
    return True

def any_uneven(items):
    """Return True if the list contains any uneven numbers"""
    for item in items: # [consider-using-any-or-all]
        if not item % 2 == 0:
            return True
    return False

def all_uneven(items):
    """Return True if the list contains all uneven numbers"""
    for item in items: # [consider-using-any-or-all]
        if item % 2 == 0:
            return False
    return True

def is_from_string(item):
    """Return True if one of parents of item is a string"""
    for parent in item.parents(): # [consider-using-any-or-all]
        if isinstance(parent, str):
            return True
    return False

def is_not_from_string(item):
    """Return True if one of parents of item isn't a string"""
    for parent in item.parents(): # [consider-using-any-or-all]
        if not isinstance(parent, str):
            return True
    return False

def nested_check(items):
    """Tests that for loops at deeper levels are picked up"""
    if items and len(items) > 5:
        print(items)
        for item in items: # [consider-using-any-or-all]
            if item in (1, 2, 3):
                return False
        return True
    print(items)
    return items[3] > 5

def words_contains_word(words):
    """Return whether words contains 'word'"""
    for word in words: # [consider-using-any-or-all]
        if word == "word":
            return True
    return False

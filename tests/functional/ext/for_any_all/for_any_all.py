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

def complicated_condition_check(items):
    """Case where we expect not any statement with a more complicated condition"""
    for item in items: # [consider-using-any-or-all]
        if item % 2 == 0 and (item % 3 == 0 or item > 15):
            return False
    return True

def is_from_decorator1(node):
    """Case where we expect a particularly long message to be emitted."""
    for ancestor in node: # [consider-using-any-or-all]
        if (
            ancestor.name in ("Exception", "BaseException")
            and ancestor.root().name == "Exception"
        ):
            return True
    return False

def is_from_decorator2(items):
    """Case where we expect an all statement because of negation in the condition"""
    for item in items: # [consider-using-any-or-all]
        if not(item % 2 == 0 and (item % 3 == 0 or item > 15)):
            return False
    return True

def is_from_decorator3(node):
    """Case where we expect a not all statement because of negation in the condition"""
    for ancestor in node: # [consider-using-any-or-all]
        if not (
            ancestor.name in ("Exception", "BaseException")
            and ancestor.root().name == "Exception"
        ):
            return True
    return False

def no_suggestion_if_not_if():
    """Do not emit if the for loop does not have the pattern we are looking for"""
    for val in range(1):
        var = val
        return var

def no_suggestion_if_not_bool(item):
    """Do not emit if the if-statement does not return a bool"""
    for parent in item.parents():
        if isinstance(parent, str):
            return "True"
    return "False"

def print_items(items):
    """Do not emit if there is no If condition in the for loop."""
    for item in items:
        print(item)
    return True

def print_items2(items):
    """Do not emit if anything besides a boolean is returned."""
    for item in items:
        return item
    return True

def print_items3(items):
    """Do not emit if anything besides a boolean is returned."""
    for _ in items:
        return False
    return items

def print_items4(items):
    """Do not emit if there is more logic which can cause side effects
    or become less readable in a list comprehension.
    """
    for item in items:
        if isinstance(item, str):
            print(item)
            return False
    return True

def is_from_decorator(node):
    """Do not emit if the if has an else condition. Generally implies more complicated logic."""
    for parent in node.node_ancestors():
        if isinstance(parent, str): # pylint: disable=no-else-return
            return True
        else:
            if parent in parent.selected_annotations:
                return False
            return False

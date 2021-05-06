"""Emit a message for iteration through dict keys and subscripting dict with key."""

# pylint: disable=missing-docstring, import-error, useless-object-inheritance, unsubscriptable-object, too-few-public-methods

def bad():
    a_dict = {1:1, 2:2, 3:3}
    for k in a_dict:# [consider-using-dict-items]
        print(a_dict[k])
    another_dict = dict()
    for k in another_dict:# [consider-using-dict-items]
        print(another_dict[k])


def good():
    a_dict = {1:1, 2:2, 3:3}
    for k in a_dict:
        print(k)

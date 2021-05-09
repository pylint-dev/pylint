"""Emit a message for iteration through dict keys and subscripting dict with key."""

# pylint: disable=missing-docstring,unsubscriptable-object

def bad():
    a_dict = {1:1, 2:2, 3:3}
    for k in a_dict: # [consider-using-dict-items]
        print(a_dict[k])
    another_dict = dict()
    for k in another_dict: # [consider-using-dict-items]
        print(another_dict[k])


def good():
    a_dict = {1:1, 2:2, 3:3}
    for k in a_dict:
        print(k)

out_of_scope_dict = dict()

def another_bad():
    for k in out_of_scope_dict: # [consider-using-dict-items]
        print(out_of_scope_dict[k])

def another_good():
    for k in out_of_scope_dict:
        k = 1
        k = 2
        k = 3
        print(out_of_scope_dict[k])

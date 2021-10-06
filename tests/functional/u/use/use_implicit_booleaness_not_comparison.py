# pylint: disable=missing-docstring, missing-module-docstring, invalid-name
# https://github.com/PyCQA/pylint/issues/4774

def github_issue_4774():
    # Test litearls
    # https://github.com/PyCQA/pylint/issues/4774
    good_list = []
    if not good_list:
        pass

    bad_list = []
    if bad_list == []: # [use-implicit-booleaness-empty-literal]
        pass

# Testing for empty literals
empty_tuple = ()
empty_list = []
empty_dict = {}

if empty_tuple == (): # [use-implicit-booleaness-empty-literal]
    pass

if empty_list == []: # [use-implicit-booleaness-empty-literal]
    pass

if empty_dict == {}: # [use-implicit-booleaness-empty-literal]
    pass

if () == empty_tuple: # [use-implicit-booleaness-empty-literal]
    pass

if [] == empty_list: # [use-implicit-booleaness-empty-literal]
    pass

if {} == empty_dict: # [use-implicit-booleaness-empty-literal]
    pass

def bad_tuple_return():
    a = (1, )
    return a == () # [use-implicit-booleaness-empty-literal]

def bad_list_return():
    a = [1]
    return a == [] # [use-implicit-booleaness-empty-literal]

def bad_dict_return():
    a = {1: 1}
    return a == {} # [use-implicit-booleaness-empty-literal]

assert () == empty_tuple # [use-implicit-booleaness-empty-literal]
assert [] == empty_list # [use-implicit-booleaness-empty-literal]
assert {} == empty_dict # [use-implicit-booleaness-empty-literal]

assert [] == []
assert {} != {}
assert () == ()

if a in {}:
    pass

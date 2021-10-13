# pylint: disable=missing-docstring, missing-module-docstring, invalid-name
# pylint: disable=too-few-public-methods, line-too-long
# https://github.com/PyCQA/pylint/issues/4774

def github_issue_4774():
    # Test litearls
    # https://github.com/PyCQA/pylint/issues/4774
    good_list = []
    if not good_list:
        pass

    bad_list = []
    if bad_list == []: # [use-implicit-booleaness-not-comparison]
        pass

# Testing for empty literals
empty_tuple = ()
empty_list = []
empty_dict = {}

if empty_tuple == (): # [use-implicit-booleaness-not-comparison]
    pass

if empty_list == []: # [use-implicit-booleaness-not-comparison]
    pass

if empty_dict == {}: # [use-implicit-booleaness-not-comparison]
    pass

if () == empty_tuple: # [use-implicit-booleaness-not-comparison]
    pass

if [] == empty_list: # [use-implicit-booleaness-not-comparison]
    pass

if {} == empty_dict: # [use-implicit-booleaness-not-comparison]
    pass

def bad_tuple_return():
    t = (1, )
    return t == () # [use-implicit-booleaness-not-comparison]

def bad_list_return():
    b = [1]
    return b == [] # [use-implicit-booleaness-not-comparison]

def bad_dict_return():
    c = {1: 1}
    return c == {} # [use-implicit-booleaness-not-comparison]

assert () == empty_tuple # [use-implicit-booleaness-not-comparison]
assert [] == empty_list # [use-implicit-booleaness-not-comparison]
assert {} != empty_dict # [use-implicit-booleaness-not-comparison]
assert () < empty_tuple # [use-implicit-booleaness-not-comparison]
assert [] <= empty_list # [use-implicit-booleaness-not-comparison]
assert () > empty_tuple # [use-implicit-booleaness-not-comparison]
assert [] >= empty_list # [use-implicit-booleaness-not-comparison]

assert [] == []
assert {} != {}
assert () == ()

d = {}

if d in {}:
    pass

class NoBool:
    def __init__(self):
        self.a = 2

class YesBool:
    def __init__(self):
        self.a = True

    def __bool__(self):
        return self.a


# Shouldn't be triggered
a = NoBool()
if [] == a:
    pass

a = YesBool()
if a == []: # [use-implicit-booleaness-not-comparison]
    pass

# compound test cases

e = []
f = {}

if e == [] and f == {}: # [use-implicit-booleaness-not-comparison, use-implicit-booleaness-not-comparison]
    pass


named_fields = [0, "", "42", "forty two"]
empty = any(field == "" for field in named_fields)

something_else = NoBool()
empty_literals = [[], {}, ()]
is_empty = any(field == something_else for field in empty_literals)

# this should work, but it doesn't since, input parameter only get the latest one, not all when inferred()
# h, i, j = 1, None, [1,2,3]

# def test(k):
    # print(k == {})

# test(h)
# test(i)
# test(j)

# pylint: disable=missing-docstring, expression-not-assigned, too-few-public-methods, bad-chained-comparison
# pylint: disable=no-member, import-error, line-too-long
# pylint: disable=unnecessary-comprehension, use-dict-literal, use-implicit-booleaness-not-comparison

from unknown import Unknown


class CustomClass:
    def keys(self):
        return []

for key in Unknown().keys():
    pass
for key in Unknown.keys():
    pass
for key in dict.keys():
    pass
for key in {}.values():
    pass
for key in {}.key():
    pass
for key in CustomClass().keys():
    pass

[key for key in {}.keys()] # [consider-iterating-dictionary]
(key for key in {}.keys()) # [consider-iterating-dictionary]
{key for key in {}.keys()} # [consider-iterating-dictionary]
{key: key for key in {}.keys()} # [consider-iterating-dictionary]
comp1 = [key for key in {}.keys()] # [consider-iterating-dictionary]
comp2 = (key for key in {}.keys()) # [consider-iterating-dictionary]
comp3 = {key for key in {}.keys()} # [consider-iterating-dictionary]
COMP4 = {key: key for key in {}.keys()} # [consider-iterating-dictionary]
for key in {}.keys(): # [consider-iterating-dictionary]
    pass

# Issue #1247
DICT = {'a': 1, 'b': 2}
comp1 = [k * 2 for k in DICT.keys()] + [k * 3 for k in DICT.keys()]  # [consider-iterating-dictionary,consider-iterating-dictionary]
comp2, comp3 = [k * 2 for k in DICT.keys()], [k * 3 for k in DICT.keys()]  # [consider-iterating-dictionary,consider-iterating-dictionary]
SOME_TUPLE = ([k * 2 for k in DICT.keys()], [k * 3 for k in DICT.keys()])  # [consider-iterating-dictionary,consider-iterating-dictionary]

# Checks for membership checks
if 1 in dict().keys(): # [consider-iterating-dictionary]
    pass
if 1 in {}.keys(): # [consider-iterating-dictionary]
    pass
if 1 in Unknown().keys():
    pass
if 1 in Unknown.keys():
    pass
if 1 in CustomClass().keys():
    pass
if 1 in dict():
    pass
if 1 in dict().values():
    pass
if (1, 1) in dict().items():
    pass
if [1] == {}.keys():
    pass
if [1] == {}:
    pass
if [1] == dict():
    pass
var = 1 in {}.keys() # [consider-iterating-dictionary]
var = 1 in {}
var = 1 in dict()
var = [1, 2] == {}.keys() in {False}

# Additional membership checks
# See: https://github.com/pylint-dev/pylint/issues/5323
METADATA = {}
if "a" not in list(METADATA.keys()): # [consider-iterating-dictionary]
    print(1)
if "a" not in METADATA.keys(): # [consider-iterating-dictionary]
    print(1)
if "a" in list(METADATA.keys()): # [consider-iterating-dictionary]
    print(1)
if "a" in METADATA.keys(): # [consider-iterating-dictionary]
    print(1)


class AClass:
    def a_function(self):
        class InnerClass:
            def another_function(self):
                def inner_function():
                    another_metadata = {}
                    print("a" not in list(another_metadata.keys())) # [consider-iterating-dictionary]
                    print("a" not in another_metadata.keys()) # [consider-iterating-dictionary]
                    print("a" in list(another_metadata.keys())) # [consider-iterating-dictionary]
                    print("a" in another_metadata.keys()) # [consider-iterating-dictionary]
                return  inner_function()
        return InnerClass().another_function()

A_DICT = {"a": 1, "b": 2, "c": 3}
A_SET = {"c", "d"}

# Test bitwise operations. These should not raise msg because removing `.keys()`
# either gives error or ends in a different result
print(A_DICT.keys() | A_SET)

if "a" in A_DICT.keys() | A_SET:
    pass

if "a" in A_DICT.keys() & A_SET:
    pass

if 1 in A_DICT.keys() ^ [1, 2]:
    pass

if "a" in A_DICT.keys() or A_SET:  # [consider-iterating-dictionary]
    pass

if "a" in A_DICT.keys() and A_SET:  # [consider-iterating-dictionary]
    pass

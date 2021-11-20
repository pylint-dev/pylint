# pylint: disable=missing-docstring, expression-not-assigned, too-few-public-methods
# pylint: disable=no-member, import-error, no-self-use, line-too-long, useless-object-inheritance
# pylint: disable=unnecessary-comprehension, use-dict-literal, use-implicit-booleaness-not-comparison

from unknown import Unknown


class CustomClass(object):
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
COMP1 = [key for key in {}.keys()] # [consider-iterating-dictionary]
COMP2 = (key for key in {}.keys()) # [consider-iterating-dictionary]
COMP3 = {key for key in {}.keys()} # [consider-iterating-dictionary]
COMP4 = {key: key for key in {}.keys()} # [consider-iterating-dictionary]
for key in {}.keys(): # [consider-iterating-dictionary]
    pass

# Issue #1247
DICT = {'a': 1, 'b': 2}
COMP1 = [k * 2 for k in DICT.keys()] + [k * 3 for k in DICT.keys()]  # [consider-iterating-dictionary,consider-iterating-dictionary]
COMP2, COMP3 = [k * 2 for k in DICT.keys()], [k * 3 for k in DICT.keys()]  # [consider-iterating-dictionary,consider-iterating-dictionary]
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
VAR = 1 in {}.keys() # [consider-iterating-dictionary]
VAR = 1 in {}
VAR = 1 in dict()
VAR = [1, 2] == {}.keys() in {False}

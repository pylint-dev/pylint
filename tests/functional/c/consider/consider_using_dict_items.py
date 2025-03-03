"""Emit a message for iteration through dict keys and subscripting dict with key."""

# pylint: disable=line-too-long,missing-docstring,unsubscriptable-object,too-few-public-methods,redefined-outer-name,use-dict-literal,modified-iterating-dict

import os


def bad():
    a_dict = {1: 1, 2: 2, 3: 3}
    for k in a_dict:  # [consider-using-dict-items]
        print(a_dict[k])
    another_dict = dict()
    for k in another_dict:  # [consider-using-dict-items]
        print(another_dict[k])


def good():
    a_dict = {1: 1, 2: 2, 3: 3}
    for k in a_dict:
        print(k)


OUT_OF_SCOPE_DICT = dict()


def another_bad():
    for k in OUT_OF_SCOPE_DICT:  # [consider-using-dict-items]
        print(OUT_OF_SCOPE_DICT[k])


def another_good():
    for k in OUT_OF_SCOPE_DICT:
        k = 1
        k = 2
        k = 3
        print(OUT_OF_SCOPE_DICT[k])


B_DICT = {}
for k2 in B_DICT:  # Should not emit warning, key access necessary
    B_DICT[k2] = 2

for k2 in B_DICT:  # Should not emit warning, key access necessary (AugAssign)
    B_DICT[k2] += 2

# Warning should be emitted in this case
for k6 in B_DICT:  # [consider-using-dict-items]
    val = B_DICT[k6]
    B_DICT[k6] = 2

for k3 in B_DICT:  # [consider-using-dict-items]
    val = B_DICT[k3]

for k4 in B_DICT.keys():  # [consider-iterating-dictionary,consider-using-dict-items]
    val = B_DICT[k4]


class Foo:
    c_dict = {}


# Should emit warning when iterating over a dict attribute of a class
for k5 in Foo.c_dict:  # [consider-using-dict-items]
    val = Foo.c_dict[k5]

c_dict = {}

# Should NOT emit warning whey key used to access a different dict
for k5 in Foo.c_dict:  # This is fine
    val = B_DICT[k5]

for k5 in Foo.c_dict:  # This is fine
    val = c_dict[k5]

# Should emit warning within a list/dict comprehension
val = {k9: B_DICT[k9] for k9 in B_DICT}  # [consider-using-dict-items]
val = [(k7, B_DICT[k7]) for k7 in B_DICT]  # [consider-using-dict-items]

# Should emit warning even when using dict attribute of a class within comprehension
val = [(k7, Foo.c_dict[k7]) for k7 in Foo.c_dict]  # [consider-using-dict-items]
val = any(True for k8 in Foo.c_dict if Foo.c_dict[k8])  # [consider-using-dict-items]

# Should emit warning when dict access done in ``if`` portion of comprehension
val = any(True for k8 in B_DICT if B_DICT[k8])  # [consider-using-dict-items]

# Should NOT emit warning whey key used to access a different dict
val = [(k7, B_DICT[k7]) for k7 in Foo.c_dict]
val = any(True for k8 in Foo.c_dict if B_DICT[k8])

# Should NOT emit warning, essentially same check as above
val = [(k7, c_dict[k7]) for k7 in Foo.c_dict]
val = any(True for k8 in Foo.c_dict if c_dict[k8])

# Should emit warning, using .keys() of Foo.c_dict
val = any(True for k8 in Foo.c_dict.keys() if Foo.c_dict[k8])  # [consider-iterating-dictionary,consider-using-dict-items]

# Test false positive described in #4630
# (https://github.com/pylint-dev/pylint/issues/4630)

D = {"key": "value"}

for k in D:  # this is fine, with the reassignment of d[k], d[k] is necessary
    D[k] += "123"
    if "1" in D[k]:  # index lookup necessary here, do not emit error
        print("found 1")

for k in D:  # if this gets rewritten to d.items(), we are back to the above problem
    D[k] = D[k] + 1
    if "1" in D[k]:  # index lookup necessary here, do not emit error
        print("found 1")

for k in D:  # [consider-using-dict-items]
    if "1" in D[k]:  # index lookup necessary here, do not emit error
        print("found 1")


# False positive in issue #9554
# https://github.com/pylint-dev/pylint/issues/9554
for var in os.environ.keys():  # [consider-iterating-dictionary]
    if var.startswith("foo_"):
        del os.environ[var]  # index lookup necessary here, do not emit error

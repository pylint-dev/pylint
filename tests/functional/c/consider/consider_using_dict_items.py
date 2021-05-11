"""Emit a message for iteration through dict keys and subscripting dict with key."""
# pylint: disable=line-too-long,missing-docstring,unsubscriptable-object,too-few-public-methods

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

out_of_scope_dict = dict()

def another_bad():
    for k in out_of_scope_dict:  # [consider-using-dict-items]
        print(out_of_scope_dict[k])

def another_good():
    for k in out_of_scope_dict:
        k = 1
        k = 2
        k = 3
        print(out_of_scope_dict[k])


b_dict = {}
for k2 in b_dict:  # Should not emit warning, key access necessary
    b_dict[k2] = 2

for k2 in b_dict:  # Should not emit warning, key access necessary (AugAssign)
    b_dict[k2] += 2

# Warning should be emitted in this case
for k6 in b_dict:  # [consider-using-dict-items]
    val = b_dict[k6]
    b_dict[k6] = 2

for k3 in b_dict:  # [consider-using-dict-items]
    val = b_dict[k3]

for k4 in b_dict.keys():  # [consider-iterating-dictionary,consider-using-dict-items]
    val = b_dict[k4]

class Foo:
    c_dict = {}

# Should emit warning when iterating over a dict attribute of a class
for k5 in Foo.c_dict:  # [consider-using-dict-items]
    val = Foo.c_dict[k5]

c_dict = {}

# Should NOT emit warning whey key used to access a different dict
for k5 in Foo.c_dict:  # This is fine
    val = b_dict[k5]

for k5 in Foo.c_dict:  # This is fine
    val = c_dict[k5]

# Should emit warning within a list/dict comprehension
val = {k9: b_dict[k9] for k9 in b_dict}  # [consider-using-dict-items]
val = [(k7, b_dict[k7]) for k7 in b_dict]  # [consider-using-dict-items]

# Should emit warning even when using dict attribute of a class within comprehension
val = [(k7, Foo.c_dict[k7]) for k7 in Foo.c_dict]  # [consider-using-dict-items]
val = any(True for k8 in Foo.c_dict if Foo.c_dict[k8])  # [consider-using-dict-items]

# Should emit warning when dict access done in ``if`` portion of comprehension
val = any(True for k8 in b_dict if b_dict[k8])  # [consider-using-dict-items]

# Should NOT emit warning whey key used to access a different dict
val = [(k7, b_dict[k7]) for k7 in Foo.c_dict]
val = any(True for k8 in Foo.c_dict if b_dict[k8])

# Should NOT emit warning, essentially same check as above
val = [(k7, c_dict[k7]) for k7 in Foo.c_dict]
val = any(True for k8 in Foo.c_dict if c_dict[k8])

# Should emit warning, using .keys() of Foo.c_dict
val = any(True for k8 in Foo.c_dict.keys() if Foo.c_dict[k8])  # [consider-iterating-dictionary,consider-using-dict-items]

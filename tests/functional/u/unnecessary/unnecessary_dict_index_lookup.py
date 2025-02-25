# pylint: disable=missing-docstring, too-few-public-methods, expression-not-assigned, line-too-long

A_DICT = {}
B_DICT = {}

for k, v in A_DICT.items():
    print(A_DICT[k])  # [unnecessary-dict-index-lookup]
    print(B_DICT[k])  # Should not emit warning, accessing other dictionary
    A_DICT[k] = 123  # Should not emit warning, key access necessary
    A_DICT[k] += 123  # Should not emit warning, key access necessary
    print(A_DICT[k])  # Should not emit warning, v != a_dict[k]

for k, v in B_DICT.items():
    print(k)
    k = "another key"
    print(B_DICT[k])  # This is fine, key reassigned


# Tests on comprehensions
A = {v: 1 for k, v in A_DICT.items() if A_DICT[k]}  # [unnecessary-dict-index-lookup]
B = {v: 1 for k, v in A_DICT.items() if k}  # This is fine, no indexing
C = {A_DICT[k]: 1 for k, v in A_DICT.items() if k}  # [unnecessary-dict-index-lookup]
# +1: [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]
D = {A_DICT[k]: 1 for k, v in A_DICT.items() if A_DICT[k]}

E = [v for k, v in A_DICT.items() if A_DICT[k]]  # [unnecessary-dict-index-lookup]
f = [v for k, v in A_DICT.items() if k]  # This is fine, no indexing
G = [A_DICT[k] for k, v in A_DICT.items() if k]  # [unnecessary-dict-index-lookup]
# +1: [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]
H = [A_DICT[k] for k, v in A_DICT.items() if A_DICT[k]]


# Tests on dict attribute of a class
class Foo:
    c_dict = {}


for k, v in Foo.c_dict.items():
    print(B_DICT[k])  # Should not emit warning, accessing other dictionary
    print(Foo.c_dict[k])  # [unnecessary-dict-index-lookup]
    unnecessary = 0  # pylint: disable=invalid-name
    unnecessary += Foo.c_dict[k]  # [unnecessary-dict-index-lookup]
    Foo.c_dict[k] += v  # key access necessary

# Tests on comprehensions
S = {v: 1 for k, v in Foo.c_dict.items() if Foo.c_dict[k]}  # [unnecessary-dict-index-lookup]
J = {v: 1 for k, v in Foo.c_dict.items() if k}  # This is fine, no indexing
K = {Foo.c_dict[k]: 1 for k, v in Foo.c_dict.items() if k}  # [unnecessary-dict-index-lookup]
# +1: [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]
L = {Foo.c_dict[k]: 1 for k, v in Foo.c_dict.items() if Foo.c_dict[k]}

M = [v for k, v in Foo.c_dict.items() if Foo.c_dict[k]]  # [unnecessary-dict-index-lookup]
N = [v for k, v in Foo.c_dict.items() if k]  # This is fine, no indexing
T = [Foo.c_dict[k] for k, v in Foo.c_dict.items() if k]  # [unnecessary-dict-index-lookup]
# +1: [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]
P = [Foo.c_dict[k] for k, v in Foo.c_dict.items() if Foo.c_dict[k]]

# Test assigning d.items() to a single variable
d = {1: "a", 2: "b"}
for item in d.items():
    print(item[0])
    print(d[item[0]])  # [unnecessary-dict-index-lookup]

Q = [item[0] for item in d.items()]
R = [d[item[0]] for item in d.items()]  # [unnecessary-dict-index-lookup]

# Reassigning single var
for item in d.items():
    print(item[0])
    print(d[item[0]])  # [unnecessary-dict-index-lookup]
    item = (2, "b")
    print(d[item[0]])  # This is fine, no warning thrown as key has been reassigned


# Test false positive described in #4630
# (https://github.com/pylint-dev/pylint/issues/4630)

d = {'key': 'value'}

for k, _ in d.items():
    d[k] += 'VALUE'
    if 'V' in d[k]:  # This is fine, if d[k] is replaced with _, the semantics change
        print('found V')


for k, _ in d.items():
    if 'V' in d[k]:  # [unnecessary-dict-index-lookup]
        d[k] = "value"
        print(d[k])  # This is fine

# Test false positive described in #4716
# Should not be emitted for del
# (https://github.com/pylint-dev/pylint/issues/4716)
d = {}
for key, val in d.items():
    del d[key]
    break

for item in d.items():
    del d[item[0]]
    break

OUTER_DICT = {"inner_dict": {}}
for key, val in OUTER_DICT.items():
    for key_two, val_two in val.items():
        del OUTER_DICT[key][key_two]  # [unnecessary-dict-index-lookup]
        break

# Test partial unpacking of items
# https://github.com/pylint-dev/pylint/issues/5504

d = {}
for key, in d.items():
    print(d[key])

# Test subscripting an attribute
# https://github.com/pylint-dev/pylint/issues/6557
f = Foo()
for input_output in d.items():
    f.input_output = input_output  # pylint: disable=attribute-defined-outside-init
    print(d[f.input_output[0]])

# Regression test for https://github.com/pylint-dev/pylint/issues/6788
d = {'a': 1, 'b': 2, 'c': 3}
for key, val in d.items():
    ([d[key], x], y) = ([1, 2], 3)

# Regression test for https://github.com/pylint-dev/pylint/issues/6818
d = {'a': 1, 'b': 2, 'c': 3}
for key, val in d.items():
    while d[key] > 0:
        d[key] -= 1

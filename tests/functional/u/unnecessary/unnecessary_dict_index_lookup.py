# pylint: disable=missing-docstring, too-few-public-methods, expression-not-assigned, line-too-long

a_dict = dict()
b_dict = dict()

for k, v in a_dict.items():
    print(a_dict[k])  # [unnecessary-dict-index-lookup]
    print(b_dict[k])  # Should not emit warning, accessing other dictionary
    a_dict[k] = 123  # Should not emit warning, key access necessary
    a_dict[k] += 123  # Should not emit warning, key access necessary
    print(a_dict[k])  # [unnecessary-dict-index-lookup]
    k = "another key"
    print(a_dict[k])  # This is fine, key reassigned


# Tests on comprehensions
{v: 1 for k, v in a_dict.items() if a_dict[k]}  # [unnecessary-dict-index-lookup]
{v: 1 for k, v in a_dict.items() if k}  # This is fine, no indexing
{a_dict[k]: 1 for k, v in a_dict.items() if k}  # [unnecessary-dict-index-lookup]
{a_dict[k]: 1 for k, v in a_dict.items() if a_dict[k]}  # [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]

[v for k, v in a_dict.items() if a_dict[k]]  # [unnecessary-dict-index-lookup]
[v for k, v in a_dict.items() if k]  # This is fine, no indexing
[a_dict[k] for k, v in a_dict.items() if k]  # [unnecessary-dict-index-lookup]
[a_dict[k] for k, v in a_dict.items() if a_dict[k]]  # [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]


# Tests on dict attribute of a class
class Foo:
    c_dict = {}

for k, v in Foo.c_dict.items():
    print(b_dict[k])  # Should not emit warning, accessing other dictionary
    print(Foo.c_dict[k])  # [unnecessary-dict-index-lookup]
    Foo.c_dict[k] += Foo.c_dict[k]  # [unnecessary-dict-index-lookup]
    Foo.c_dict[k] += v  # key access necessary

# Tests on comprehensions
{v: 1 for k, v in Foo.c_dict.items() if Foo.c_dict[k]}  # [unnecessary-dict-index-lookup]
{v: 1 for k, v in Foo.c_dict.items() if k}  # This is fine, no indexing
{Foo.c_dict[k]: 1 for k, v in Foo.c_dict.items() if k}  # [unnecessary-dict-index-lookup]
{Foo.c_dict[k]: 1 for k, v in Foo.c_dict.items() if Foo.c_dict[k]}  # [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]

[v for k, v in Foo.c_dict.items() if Foo.c_dict[k]]  # [unnecessary-dict-index-lookup]
[v for k, v in Foo.c_dict.items() if k]  # This is fine, no indexing
[Foo.c_dict[k] for k, v in Foo.c_dict.items() if k]  # [unnecessary-dict-index-lookup]
[Foo.c_dict[k] for k, v in Foo.c_dict.items() if Foo.c_dict[k]]  # [unnecessary-dict-index-lookup, unnecessary-dict-index-lookup]

# Test assigning d.items() to a single variable
d = {1: "a", 2: "b"}
for item in d.items():
    print(item[0])
    print(d[item[0]])  # [unnecessary-dict-index-lookup]

[item[0] for item in d.items()]
[d[item[0]] for item in d.items()]  # [unnecessary-dict-index-lookup]

# Reassigning single var
for item in d.items():
    print(item[0])
    print(d[item[0]])  # [unnecessary-dict-index-lookup]
    item = (2, "b")
    print(d[item[0]])  # This is fine, no warning thrown as key has been reassigned

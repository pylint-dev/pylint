"""Tests for potential-index-error"""
# pylint: disable=invalid-name, undefined-variable, missing-function-docstring, unused-variable

# Check assignment on same line
index = 3
print([1, 2, 3][3])  # [potential-index-error]
print((1, 2, 3)[3])  # [potential-index-error]
print([1, 2, 3][index])  # [potential-index-error]

# Check assignment on previous line
# We (currently) do not raise here to avoid risks of false positives
a_list = [1, 2, 3]
print(a_list[3])

# Test for uninferable lists
def my_func():
    an_inner_list = [1, 2, 3]


print(an_inner_list[3])


# Test that we don't crash on more complicated indices/slices
# We do not raise here (currently)
print([1, 2, 3][2:3])


# Test for cases with unpacking operation
my_list = ["foo", "bar"]
my_set = {"foo", "bar"}
my_tuple = ("foo", "bar")
my_iterable = (*my_list, *my_set, *my_tuple, *("foo", "bar"))
my_non_iterable = None

print([*my_list][1])
print([*my_list][2])  # [potential-index-error]

print([*my_set][1])
print([*my_set][2])  # [potential-index-error]

print((*my_tuple,)[1])
print((*my_tuple,)[2])  # [potential-index-error]

print((*my_iterable,)[7])
print((*my_iterable,)[8])  # [potential-index-error]

print((*my_non_iterable,)[0])
print((*my_non_iterable,)[1])  # [potential-index-error]

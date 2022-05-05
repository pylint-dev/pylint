"""Tests for unnecessary-list-index-lookup with assignment expressions."""

# pylint: disable=missing-docstring, too-few-public-methods, expression-not-assigned, line-too-long, unused-variable

my_list = ['a', 'b']

for idx, val in enumerate(my_list):
    if (val := 42) and my_list[idx] == 'b':
        print(1)

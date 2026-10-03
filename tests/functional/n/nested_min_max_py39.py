"""Test detection of redundant nested calls to min/max functions"""

# pylint: disable=redefined-builtin,unnecessary-lambda-assignment

max(3, max({1: 2} | {i: i for i in range(4) if i}))  # [nested-min-max]
max(3, *{1: 2} | {i: i for i in range(4) if i})

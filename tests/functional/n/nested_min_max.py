"""Test detection of redundant nested calls to min/max functions"""


min(1, min(2, 3))  # [nested-min-max]
max(1, max(2, 3))  # [nested-min-max]
min(min(1, 2), 3)  # [nested-min-max]
min(min(min(1, 2), 3), 4)  # [nested-min-max]
min(1, max(2, 3))
min(1, 2, 3)
min(min(1, 2), min(3, 4))  # [nested-min-max]
min(len([]), min(len([1]), len([1, 2])))  # [nested-min-max]

orig_min = min
min = lambda *args: args[0]  # pylint: disable=redefined-builtin,unnecessary-lambda-assignment
min(1, min(2, 3))
orig_min(1, orig_min(2, 3))  # [nested-min-max]

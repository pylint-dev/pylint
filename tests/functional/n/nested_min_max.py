"""Test detection of redundant nested calls to min/max functions"""

# pylint: disable=redefined-builtin,unnecessary-lambda-assignment

min(1, min(2, 3))  # [nested-min-max]
max(1, max(2, 3))  # [nested-min-max]
min(min(1, 2), 3)  # [nested-min-max]
min(min(min(1, 2), 3), 4)  # [nested-min-max, nested-min-max]
min(1, max(2, 3))
min(1, 2, 3)
min(min(1, 2), min(3, 4))  # [nested-min-max]
min(len([]), min(len([1]), len([1, 2])))  # [nested-min-max]

orig_min = min
min = lambda *args: args[0]
min(1, min(2, 3))
orig_min(1, orig_min(2, 3))  # [nested-min-max]

# This is too complicated (for now) as there is no clear better way to write it
max(max(i for i in range(10)), 0)
max(max(max(i for i in range(10)), 0), 1)

# These examples can be improved by splicing
lst = [1, 2]
max(3, max(lst))  # [nested-min-max]
max(3, *lst)

nums = (1, 2,)
max(3, max(nums))  # [nested-min-max]
max(3, *nums)

nums = {1, 2}
max(3, max(nums))  # [nested-min-max]
max(3, *nums)

nums = {1: 2, 7: 10}
max(3, max(nums))  # [nested-min-max]
max(3, *nums)

max(3, max(nums.values()))  # [nested-min-max]
max(3, *nums.values())

lst2 = [3, 7, 10]
max(3, max(nums), max(lst2))  # [nested-min-max]

max(3, max([5] + [6, 7]))  # [nested-min-max]
max(3, *[5] + [6, 7])

max(3, max([5] + [i for i in range(4) if i]))  # [nested-min-max]
max(3, *[5] + [i for i in range(4) if i])

max(3, max([5] + list(range(4))))  # [nested-min-max]
max(3, *[5] + list(range(4)))

max(3, max(list(range(4))))  # [nested-min-max]
max(3, *list(range(4)))

# Nesting is useful for finding the maximum in a matrix
# No message if external call has exactly 1 argument
matrix = [[1, 2, 3], [4, 5, 6]]
max(max(matrix))
max(max(max(matrix)))
max(3, max(max(matrix)))  # [nested-min-max]
max(max(3, max(matrix)))  # [nested-min-max]

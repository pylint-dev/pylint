"""All of these nested-min-max messages should suggest splatting."""

lst = [1, 2]
max(3, max(lst))  # [nested-min-max]

nums = (1, 2,)
max(3, max(nums))  # [nested-min-max]

nums = {1, 2}
max(3, max(nums))  # [nested-min-max]

nums = {1: 2, 7: 10}
max(3, max(nums))  # [nested-min-max]

max(3, max(nums.values()))  # [nested-min-max]

lst2 = [3, 7, 10]
max(3, max(nums), max(lst2))  # [nested-min-max]

"""Tests for unnecessary-list-index-lookup."""

# pylint: disable=missing-docstring, too-few-public-methods, expression-not-assigned, line-too-long, unused-variable

my_list = ['a', 'b']

for idx, val in enumerate(my_list):
    print(my_list[idx]) # [unnecessary-list-index-lookup]

for idx, _ in enumerate(my_list):
    print(my_list[0])
    if idx > 0:
        print(my_list[idx - 1])

for idx, val in enumerate(my_list):
    del my_list[idx]

for idx, val in enumerate(my_list):
    my_list[idx] = 42

for vals in enumerate(my_list):
    # This could be refactored, but too complex to infer
    print(my_list[vals[0]])

def process_list(data):
    for index, value in enumerate(data):
        index = 1
        print(data[index])

def process_list_again(data):
    for index, value in enumerate(data):
        value = 1
        print(data[index]) # Can't use value here, it's been redefined

other_list = [1, 2]
for idx, val in enumerate(my_list):
    print(other_list[idx])

OTHER_INDEX = 0
for idx, val in enumerate(my_list):
    print(my_list[OTHER_INDEX])

result = [val for idx, val in enumerate(my_list) if my_list[idx] == 'a'] # [unnecessary-list-index-lookup]
result = [val for idx, val in enumerate(my_list) if idx > 0 and my_list[idx - 1] == 'a']
result = [val for idx, val in enumerate(my_list) if other_list[idx] == 'a']
result = [my_list[idx] for idx, val in enumerate(my_list)] # [unnecessary-list-index-lookup]

# Regression test for https://github.com/pylint-dev/pylint/issues/6049
pairs = [(0, 0)]
for i, (a, b) in enumerate(pairs):
    print(pairs[i][0])

# Regression test for https://github.com/pylint-dev/pylint/issues/6603
for i, num in enumerate():  # raises TypeError, but shouldn't crash pylint
    pass

# Regression test for https://github.com/pylint-dev/pylint/issues/6788
num_list = [1, 2, 3]
for a, b in enumerate(num_list):
    num_list[a], _ = (2, 1)

num_list = [1, 2, 3]
for a, b in enumerate(num_list):
    ([x, num_list[a]], _) = ([5, 6], 1)

# Regression test for https://github.com/pylint-dev/pylint/issues/6818
updated_list = [1, 2, 3]
for idx, val in enumerate(updated_list):
    while updated_list[idx] > 0:
        updated_list[idx] -= 1

updated_list = [1, 2, 3]
for idx, val in enumerate(updated_list):
    print(updated_list[idx]) # [unnecessary-list-index-lookup]
    updated_list[idx] -= 1
    print(updated_list[idx])

# Regression test for https://github.com/pylint-dev/pylint/issues/6896
parts = ["a", "b", "c", "d"]
for i, part in enumerate(parts):
    if i == 3:  # more complex condition actually
        parts.insert(i, "X")
    print(part, parts[i])

# regression tests for https://github.com/pylint-dev/pylint/issues/7682
series = [1, 2, 3, 4, 5]
output_list = [
    (item, series[index])
    for index, item in enumerate(series, start=1)
    if index < len(series)
]

output_list = [
    (item, series[index])
    for index, item in enumerate(series, 1)
    if index < len(series)
]

for idx, val in enumerate(series, start=2):
    print(series[idx])

for idx, val in enumerate(series, 2):
    print(series[idx])

for idx, val in enumerate(series, start=-2):
    print(series[idx])

for idx, val in enumerate(series, -2):
    print(series[idx])

for idx, val in enumerate(series, start=0):
    print(series[idx])  # [unnecessary-list-index-lookup]

for idx, val in enumerate(series, 0):
    print(series[idx])  # [unnecessary-list-index-lookup]

START = 0
for idx, val in enumerate(series, start=START):
    print(series[idx])  # [unnecessary-list-index-lookup]

for idx, val in enumerate(series, START):
    print(series[idx])  # [unnecessary-list-index-lookup]

START = [1, 2, 3]
for i, k in enumerate(series, len(START)):
    print(series[idx])

def return_start(start):
    return start

for i, k in enumerate(series, return_start(20)):
    print(series[idx])

for idx, val in enumerate(iterable=series, start=0):
    print(series[idx])  # [unnecessary-list-index-lookup]

result = [my_list[idx] for idx, val in enumerate(iterable=my_list)]  # [unnecessary-list-index-lookup]

iterable_kwarg = {"iterable": my_list}
result = [my_list[idx] for idx, val in enumerate(**iterable_kwarg)]  # [unnecessary-list-index-lookup]

for idx, val in enumerate():
    print(my_list[idx])

class Command:
    def _get_extra_attrs(self, extra_columns):
        self.extra_rows_start = 8  # pylint: disable=attribute-defined-outside-init
        for index, column in enumerate(extra_columns, start=self.extra_rows_start):
            pass

Y_START = 2
nums = list(range(20))
for y, x in enumerate(nums, start=Y_START + 1):
    pass

for idx, val in enumerate(my_list):
    if (val := 42) and my_list[idx] == 'b':
        print(1)

def regression_9078(apples, cant_infer_this):
    """Regression test for https://github.com/pylint-dev/pylint/issues/9078."""
    for _, _ in enumerate(apples, int(cant_infer_this)):
        ...

def random_uninferrable_start(pears):
    import random # pylint: disable=import-outside-toplevel

    for _, _ in enumerate(pears, random.choice([5, 42])):
        ...

"""Tests for unnecessary-list-index-lookup."""

# pylint: disable=missing-docstring, too-few-public-methods, expression-not-assigned, line-too-long, unused-variable

MY_LIST = ['a', 'b']

for idx, val in enumerate(MY_LIST):
    print(MY_LIST[idx]) # [unnecessary-list-index-lookup]

for idx, _ in enumerate(MY_LIST):
    print(MY_LIST[0])
    if idx > 0:
        print(MY_LIST[idx - 1])

for idx, val in enumerate(MY_LIST):
    del MY_LIST[idx]

for idx, val in enumerate(MY_LIST):
    MY_LIST[idx] = 42

for vals in enumerate(MY_LIST):
    # This could be refactored, but too complex to infer
    print(MY_LIST[vals[0]])

def process_list(data):
    for index, value in enumerate(data):
        index = 1
        print(data[index])

def process_list_again(data):
    for index, value in enumerate(data):
        value = 1
        print(data[index]) # Can't use value here, it's been redefined

OTHER_LIST = [1, 2]
for idx, val in enumerate(MY_LIST):
    print(OTHER_LIST[idx])

OTHER_INDEX = 0
for idx, val in enumerate(MY_LIST):
    print(MY_LIST[OTHER_INDEX])

result = [val for idx, val in enumerate(MY_LIST) if MY_LIST[idx] == 'a'] # [unnecessary-list-index-lookup]
result = [val for idx, val in enumerate(MY_LIST) if idx > 0 and MY_LIST[idx - 1] == 'a']
result = [val for idx, val in enumerate(MY_LIST) if OTHER_LIST[idx] == 'a']
result = [MY_LIST[idx] for idx, val in enumerate(MY_LIST)] # [unnecessary-list-index-lookup]

# Regression test for https://github.com/pylint-dev/pylint/issues/6049
PAIRS = [(0, 0)]
for i, (a, b) in enumerate(PAIRS):
    print(PAIRS[i][0])

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
PARTS = ["a", "b", "c", "d"]
for i, part in enumerate(PARTS):
    if i == 3:  # more complex condition actually
        PARTS.insert(i, "X")
    print(part, PARTS[i])

# regression tests for https://github.com/pylint-dev/pylint/issues/7682
SERIES = [1, 2, 3, 4, 5]
output_list = [
    (item, SERIES[index])
    for index, item in enumerate(SERIES, start=1)
    if index < len(SERIES)
]

output_list = [
    (item, SERIES[index])
    for index, item in enumerate(SERIES, 1)
    if index < len(SERIES)
]

for idx, val in enumerate(SERIES, start=2):
    print(SERIES[idx])

for idx, val in enumerate(SERIES, 2):
    print(SERIES[idx])

for idx, val in enumerate(SERIES, start=-2):
    print(SERIES[idx])

for idx, val in enumerate(SERIES, -2):
    print(SERIES[idx])

for idx, val in enumerate(SERIES, start=0):
    print(SERIES[idx])  # [unnecessary-list-index-lookup]

for idx, val in enumerate(SERIES, 0):
    print(SERIES[idx])  # [unnecessary-list-index-lookup]

start = 0
for idx, val in enumerate(SERIES, start=start):
    print(SERIES[idx])  # [unnecessary-list-index-lookup]

for idx, val in enumerate(SERIES, start):
    print(SERIES[idx])  # [unnecessary-list-index-lookup]

start = [1, 2, 3]
for i, k in enumerate(SERIES, len(start)):
    print(SERIES[idx])

def return_start(start_val):
    return start_val

for i, k in enumerate(SERIES, return_start(20)):
    print(SERIES[idx])

for idx, val in enumerate(iterable=SERIES, start=0):
    print(SERIES[idx])  # [unnecessary-list-index-lookup]

result = [MY_LIST[idx] for idx, val in enumerate(iterable=MY_LIST)]  # [unnecessary-list-index-lookup]

ITERABLE_KWARG = {"iterable": MY_LIST}
result = [MY_LIST[idx] for idx, val in enumerate(**ITERABLE_KWARG)]  # [unnecessary-list-index-lookup]

for idx, val in enumerate():
    print(MY_LIST[idx])

class Command:
    def _get_extra_attrs(self, extra_columns):
        self.extra_rows_start = 8  # pylint: disable=attribute-defined-outside-init
        for index, column in enumerate(extra_columns, start=self.extra_rows_start):
            pass

Y_START = 2
NUMS = list(range(20))
for y, x in enumerate(NUMS, start=Y_START + 1):
    pass

for idx, val in enumerate(MY_LIST):
    if (val := 42) and MY_LIST[idx] == 'b':
        print(1)

def regression_9078(apples, cant_infer_this):
    """Regression test for https://github.com/pylint-dev/pylint/issues/9078."""
    for _, _ in enumerate(apples, int(cant_infer_this)):
        ...

def random_uninferrable_start(pears):
    import random # pylint: disable=import-outside-toplevel

    for _, _ in enumerate(pears, random.choice([5, 42])):
        ...

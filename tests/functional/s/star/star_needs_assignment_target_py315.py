"""PEP 798 unpacking in comprehensions (Python 3.15) is valid and must not
trigger star-needs-assignment-target."""

# pylint: disable=missing-function-docstring


def transform(lists, dicts):
    starred_list = [*sub for sub in lists]
    starred_set = {*sub for sub in lists}
    double_starred_dict = {**d for d in dicts}
    starred_gen = list(*sub for sub in lists)
    return starred_list, starred_set, double_starred_dict, starred_gen

"""
Checks that only valid values are used in a mapping context.
"""
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
from __future__ import print_function


def test(**kwargs):
    print(kwargs)


# dictionary value/comprehension
dict_value = dict(a=1, b=2, c=3)
dict_comp = {chr(x): x for x in range(256)}
test(**dict_value)
test(**dict_comp)


# in order to be used in kwargs custom mapping class should define
# __iter__(), __getitem__(key) and keys().
class CustomMapping(object):
    def __init__(self):
        self.data = dict(a=1, b=2, c=3, d=4, e=5)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return self.data.keys()

test(**CustomMapping())

test(**CustomMapping)  # [not-a-mapping]

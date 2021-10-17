""" Dictionaries are reversible starting on python 3.8"""

# pylint: disable=missing-docstring
reversed({'a': 1, 'b': 2}) # [bad-reversed-sequence]

class InheritDict(dict):
    pass

reversed(InheritDict({'a': 1, 'b': 2})) # [bad-reversed-sequence]

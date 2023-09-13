""" Dictionaries are reversible starting on python 3.8"""
# pylint: disable=missing-docstring

# This can't be detected since changes to locals aren't backported
reversed({'a': 1, 'b': 2})


class InheritDict(dict):
    pass


reversed(InheritDict({'a': 1, 'b': 2})) # [bad-reversed-sequence]

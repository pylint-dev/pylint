""" Dictionaries are reversible starting on python 3.8"""
reversed({'a': 1, 'b': 2})

class InheritDict(dict):
    """Inherits from dict"""

reversed(InheritDict({'a': 1, 'b': 2}))

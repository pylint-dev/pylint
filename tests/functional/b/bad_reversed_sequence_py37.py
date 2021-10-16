""" Dictionaries are reversible starting on python 3.8"""
reversed({'a': 1, 'b': 2}) # [bad-reversed-sequence]

class InheritDict(dict):
    pass

reversed(InheritDict({'a': 1, 'b': 2})) # [bad-reversed-sequence]

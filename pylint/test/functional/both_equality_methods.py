# pylint: disable=too-few-public-methods,missing-docstring
"""
Check that a class defines both or neither of __eq__ and __ne__.
"""


class MissingNe(object): # [both-equality-methods]
    def __eq__(self, other):
        pass


class MissingEq(object): # [both-equality-methods]
    def __ne__(self, other):
        pass


class HasBoth(object):
    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass


class HasNeither(object):
    pass

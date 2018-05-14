# pylint: disable=missing-docstring,expression-not-assigned,too-few-public-methods,pointless-statement

class Unhashable(object):
    __hash__ = list.__hash__

{}[[]] # [unhashable-dict-key]
{}[{}] # [unhashable-dict-key]
{}[Unhashable()] # [unhashable-dict-key]

# pylint: disable=missing-docstring,expression-not-assigned,too-few-public-methods,pointless-statement, useless-object-inheritance


class Unhashable(object):
    __hash__ = list.__hash__

{}[[1, 2, 3]] # [unhashable-dict-key]
{}[{}] # [unhashable-dict-key]
{}[Unhashable()] # [unhashable-dict-key]
{'foo': 'bar'}['foo']
{'foo': 'bar'}[42]

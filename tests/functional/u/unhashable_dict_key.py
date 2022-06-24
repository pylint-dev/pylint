# pylint: disable=missing-docstring,expression-not-assigned,too-few-public-methods,pointless-statement, useless-object-inheritance


class Unhashable(object):
    __hash__ = list.__hash__

# Subscripts
{}[[1, 2, 3]] # [unhashable-dict-key]
{}[{}] # [unhashable-dict-key]
{}[Unhashable()] # [unhashable-dict-key]
{}[1:2]  # [unhashable-dict-key]
{'foo': 'bar'}['foo']
{'foo': 'bar'}[42]

# Keys
{[1, 2, 3]: "tomato"}  # [unhashable-dict-key]
{
    [1, 2, 3]: "tomato",  # [unhashable-dict-key]
    [4, 5, 6]: "celeriac",  # [unhashable-dict-key]
}
{"tomato": "tomahto"}

# pylint: disable=missing-docstring,expression-not-assigned,too-few-public-methods,pointless-statement, useless-object-inheritance


class Unhashable(object):
    __hash__ = list.__hash__

# Subscripts
{}[[1, 2, 3]] # [unhashable-member]
{}[{}] # [unhashable-member]
{}[Unhashable()] # [unhashable-member]
{}[1:2]  # [unhashable-member]
{'foo': 'bar'}['foo']
{'foo': 'bar'}[42]

# Keys
{[1, 2, 3]: "tomato"}  # [unhashable-member]
{
    [1, 2, 3]: "tomato",  # [unhashable-member]
    [4, 5, 6]: "celeriac",  # [unhashable-member]
}
{[1, 2, 3]}  # [unhashable-member]
{"tomato": "tomahto"}
{dict: {}}

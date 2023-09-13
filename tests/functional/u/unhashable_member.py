# pylint: disable=missing-docstring,expression-not-assigned,too-few-public-methods,pointless-statement


class Unhashable:
    __hash__ = list.__hash__

# Subscripts
{}[[1, 2, 3]] # [unhashable-member]
{}[{}] # [unhashable-member]
{}[Unhashable()] # [unhashable-member]
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
{lambda x: x: "tomato"}  # pylint: disable=unnecessary-lambda


class FromDict(dict):
    ...

{FromDict: 1}

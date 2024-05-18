"""Check trailing comma tuple optimization."""
# pylint: disable=missing-docstring

AAA = 1,
BBB = "aaaa",
CCC="aaa",
FFF=['f'],

def some_func(first, second):
    if first:
        return first,
    if second:
        return (first, second,)
    return first, second,

#pylint:enable = trailing-comma-tuple
AAA = 1,  # [trailing-comma-tuple]
BBB = "aaaa", # [trailing-comma-tuple]
# pylint: disable=trailing-comma-tuple
CCC="aaa",
III = some_func(0,
    0),
# pylint: enable=trailing-comma-tuple
FFF=['f'], # [trailing-comma-tuple]

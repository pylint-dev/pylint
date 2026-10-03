"""Check trailing comma tuple optimization."""
# pylint: disable=missing-docstring

aaa = 1,
bbb = "aaaa",
ccc="aaa",
fff=['f'],

def some_func(first, second):
    if first:
        return first,
    if second:
        return (first, second,)
    return first, second,

#pylint:enable = trailing-comma-tuple
aaa = 1,  # [trailing-comma-tuple]
bbb = "aaaa", # [trailing-comma-tuple]
# pylint: disable=trailing-comma-tuple
ccc="aaa",
III = some_func(0,
    0),
# pylint: enable=trailing-comma-tuple
fff=['f'], # [trailing-comma-tuple]

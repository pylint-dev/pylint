"""Check trailing comma one element tuples."""
# pylint: disable=bad-whitespace, missing-docstring
AAA = 1, # [trailing-comma-tuple]
BBB = "aaaa", # [trailing-comma-tuple]
CCC="aaa", # [trailing-comma-tuple]
FFF=['f'], # [trailing-comma-tuple]

BBB = 1, 2
CCC = (1, 2, 3)
DDD = (
    1, 2, 3,
)
EEE = (
    "aaa",
)


def test(*args, **kwargs):
    return args, kwargs


test(widget=1, label='test')
test(widget=1,
     label='test')
test(widget=1, \
     label='test')


def some_func(first, second):
    if first:
        return first, # [trailing-comma-tuple]
    if second:
        return (first, second,)
    return first, second,  # [trailing-comma-tuple]


def some_other_func():
    yield 'hello',  # [trailing-comma-tuple]

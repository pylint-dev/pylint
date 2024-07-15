"""Check trailing comma one element tuples."""
# pylint: disable=missing-docstring
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

GGG = ["aaa"
], # [trailing-comma-tuple]

HHH = ["aaa"
]

III = some_func(0,
    0), # [trailing-comma-tuple]

JJJ = some_func(0,
    0)

# pylint: disable-next=trailing-comma-tuple
AAA = 1,
BBB = "aaaa", # [trailing-comma-tuple]
# pylint: disable=trailing-comma-tuple
CCC="aaa",
III = some_func(0,
    0),
# pylint: enable=trailing-comma-tuple
FFF=['f'], # [trailing-comma-tuple]

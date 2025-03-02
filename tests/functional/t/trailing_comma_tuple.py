"""Check trailing comma one element tuples."""
# pylint: disable=missing-docstring
aaa = 1, # [trailing-comma-tuple]
bbb = "aaaa", # [trailing-comma-tuple]
ccc="aaa", # [trailing-comma-tuple]
fff=['f'], # [trailing-comma-tuple]

bbb = 1, 2
ccc = (1, 2, 3)
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

iii = some_func(0,
    0), # [trailing-comma-tuple]

JJJ = some_func(0,
    0)

# pylint: disable-next=trailing-comma-tuple
aaa = 1,
bbb = "aaaa", # [trailing-comma-tuple]
# pylint: disable=trailing-comma-tuple
ccc="aaa",
iii = some_func(0,
    0),
# pylint: enable=trailing-comma-tuple
fff=['f'], # [trailing-comma-tuple]

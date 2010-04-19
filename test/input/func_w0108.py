# pylint: disable=W0142
"""test suspicious lambda expressions
"""

__revision__ = ''

# Some simple examples of the most commonly encountered forms.
_ = lambda: list()  # replaceable with "list"
_ = lambda x: hash(x)  # replaceable with "hash"
_ = lambda x, y: min(x, y)  # replaceable with "min"

# A function that can take any arguments given to it.
_ANYARGS = lambda *args, **kwargs: 'completely arbitrary return value'

# Some more complex forms of unnecessary lambda expressions.
_ = lambda *args: _ANYARGS(*args)
_ = lambda **kwargs: _ANYARGS(**kwargs)
_ = lambda *args, **kwargs: _ANYARGS(*args, **kwargs)
_ = lambda x, y, z, *args, **kwargs: _ANYARGS(x, y, z, *args, **kwargs)

# Lambdas that are *not* unnecessary and should *not* trigger warnings.
_ = lambda x: x
_ = lambda x: x()
_ = lambda x = 4: hash(x)
_ = lambda x, y: range(y, x)
_ = lambda x: range(5, x)
_ = lambda x, y: range(x, 5)
_ = lambda x, y, z: x.y(z)
_ = lambda: 5
_ = lambda **kwargs: _ANYARGS()
_ = lambda **kwargs: _ANYARGS(**dict([('three', 3)]))
_ = lambda **kwargs: _ANYARGS(**{'three': 3})
_ = lambda dict_arg, **kwargs: _ANYARGS(kwargs, **dict_arg)
_ = lambda *args: _ANYARGS()
_ = lambda *args: _ANYARGS(*list([3, 4]))
_ = lambda *args: _ANYARGS(*[3, 4])
_ = lambda list_arg, *args: _ANYARGS(args, *list_arg)
_ = lambda: _ANYARGS(*[3])
_ = lambda: _ANYARGS(**{'three': 3})
_ = lambda: _ANYARGS(*[3], **{'three': 3})

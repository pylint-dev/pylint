# pylint: disable=missing-docstring, invalid-name

x = tuple()  # [use-tuple-literal]
x = tuple(['foo', 'bar'])  # [use-tuple-literal]
x = tuple([2, 3, 5, 8, 11])  # [use-tuple-literal]
x = ()
x = (1, 2, 3)
x = ('abc', 'def')

"""
https://github.com/pylint-dev/pylint/issues/3507
False-positive 'isinstance-second-argument-not-valid-type'
for typing aliases in 'isinstance' calls.
"""
import collections
import collections.abc
import typing

isinstance(42, typing.Dict)
isinstance(42, typing.Counter)
isinstance(42, typing.Collection)
isinstance(42, typing.Iterator)
isinstance(42, typing.Tuple)
isinstance(42, typing.Callable)
isinstance(42, typing.Type)


# For comparison - also valid calls
isinstance(42, dict)
isinstance(42, collections.Counter)
isinstance(42, collections.abc.Collection)
isinstance(42, collections.abc.Iterator)
isinstance(42, tuple)
isinstance(42, collections.abc.Callable)
isinstance(42, type)

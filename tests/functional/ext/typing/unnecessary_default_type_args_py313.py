# pylint: disable=missing-docstring,deprecated-typing-alias
import collections.abc as ca
import typing as t

a1: t.Generator[int, str, str]
a2: t.Generator[int, None, None]  # [unnecessary-default-type-args]
a3: t.Generator[int]
b1: t.AsyncGenerator[int, str]
b2: t.AsyncGenerator[int, None]  # [unnecessary-default-type-args]
b3: t.AsyncGenerator[int]

c1: ca.Generator[int, str, str]
c2: ca.Generator[int, None, None]  # [unnecessary-default-type-args]
c3: ca.Generator[int]
d1: ca.AsyncGenerator[int, str]
d2: ca.AsyncGenerator[int, None]  # [unnecessary-default-type-args]
d3: ca.AsyncGenerator[int]

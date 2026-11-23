"""Trailing tool pragmas must not count toward line length.

See issue #10172 for the rationale behind this behaviour.
"""
# pylint: disable=invalid-name

# The lines below only exceed the 60 character limit because
# of a trailing tool pragma, so no message is expected here.
a1 = "a compact but readable pragma sample"  # type: ignore
a2 = "a compact but readable pragma sample"  # type: ignore[assignment]
a3 = "a compact but readable pragma sample"  # pyright: ignore
a4 = "a compact but readable pragma sample"  # pyright: ignore[reportArgumentType]
a5 = "a compact but readable pragma sample"  # noqa
a6 = "a compact but readable pragma sample"  # noqa: E501, RUF001
a7 = "a compact but readable pragma sample"  # pragma: no cover
a8 = "a compact but readable pragma sample"  # pragma: no branch
a9 = "a compact pragma sample"  # noqa: E501  # pragma: no cover

# The code is still too long once the pragma is discounted,
# so the message is still emitted, using the length of the
# code without the pragma.
# +1: [line-too-long]
b1 = "this value is deliberately made long enough to exceed the limit"  # noqa

# A word that only looks like a pragma is not stripped.
# +1: [line-too-long]
c1 = "this value is long enough to trip the limit on its own here"  # noqario

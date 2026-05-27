"""Regression test for https://github.com/pylint-dev/pylint/issues/9833.

``no-member`` should not be emitted when the accessed attribute might be
provided at runtime by a dynamic ``__getattr__`` on *any* of the inferred
owners, even when the value is inferred to a union of several types.
"""
# pylint: disable=missing-docstring,too-few-public-methods


class WithoutGetattr:
    pass


class WithGetattr:
    def __getattr__(self, name):
        return None


def factory(flag) -> "WithoutGetattr | WithGetattr":
    if flag:
        return WithoutGetattr()
    return WithGetattr()


value = factory(False)
print(value.any_attribute)  # no-member must not be emitted here

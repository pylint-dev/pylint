"""Regression test for https://github.com/pylint-dev/pylint/issues/11356.

An owner whose attribute lookup raises an ``InferenceError`` tells us nothing,
so it must not be dropped from the inferred owners: the remaining ones would
then be judged alone and ``no-member`` would be emitted for them.
"""
# pylint: disable=missing-docstring,too-few-public-methods,undefined-variable


class Meta(type):
    pass


class WithAttribute(metaclass=Meta):
    attribute = 1


class WithoutAttribute:
    pass


def factory(flag):
    if flag:
        return WithAttribute
    return WithoutAttribute


OWNER = factory(False)
print(OWNER.attribute)  # no-member must not be emitted here


# Breaks the metaclass lookup of ``WithAttribute.attribute`` above.
for Meta.attribute in _:
    pass

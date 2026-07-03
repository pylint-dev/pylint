"""Since Python version 3.8, a class decorated with typing.final cannot be
subclassed."""

# pylint: disable=missing-docstring, too-few-public-methods

# Disabled because of a bug with pypy 3.8 see
# https://github.com/pylint-dev/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements

from typing import final


@final
class Base:
    pass


class Subclass(Base):  # [subclassed-final-class]
    pass

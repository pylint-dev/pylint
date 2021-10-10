"""Since Python version 3.8, a class decorated with typing.final cannot be
subclassed """

# pylint: disable=no-init, import-error, invalid-name, using-constant-test, useless-object-inheritance
# pylint: disable=missing-docstring, too-few-public-methods

from typing import final


@final
class Base:
    pass


class Subclass(Base): # [subclassed-final-class]
    pass

"""A class decorated with typing.final cannot be subclassed """

# pylint: disable=no-init, import-error, invalid-name, using-constant-test, useless-object-inheritance
# pylint: disable=missing-docstring, too-few-public-methods, no-name-in-module using-final-in-unsupported-version

from typing import final


@final
class Base:
    pass


class Subclass(Base): # [subclassed-final-class]
    pass

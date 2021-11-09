"""Since Python version 3.8, a method decorated with typing.final cannot be
overridden"""

# pylint: disable=no-init, useless-object-inheritance, missing-docstring, too-few-public-methods

from typing import final

class Base:
    @final
    def my_method(self):
        pass


class Subclass(Base):
    def my_method(self): # [overridden-final-method]
        pass

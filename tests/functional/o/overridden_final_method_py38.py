"""Since Python version 3.8, a method decorated with typing.final cannot be
overridden"""

# pylint: disable=missing-docstring, too-few-public-methods

from typing import final

class Base:
    @final
    def my_method(self):
        pass


class Subclass(Base):
    def my_method(self): # [overridden-final-method]
        pass

# Check for crash on method definitions not at top level of class
# https://github.com/pylint-dev/pylint/issues/5648
class BaseConditional:

    create_final_method = True
    if create_final_method:
        @final
        def my_method(self):
            pass

class Subclass2(BaseConditional):

    def my_method(self): # [overridden-final-method]
        pass

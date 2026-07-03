"""Example checker detecting deprecated functions/methods. Following example searches for usages of
deprecated function `deprecated_function` and deprecated method `MyClass.deprecated_method`
from module mymodule:

.. code-block:: console
    $ cat mymodule.py
    def deprecated_function():
        pass

    def myfunction(arg0, arg1, deprecated_arg1=None, arg2='foo', arg3='bar', deprecated_arg2='spam'):
        pass

    class MyClass:
        def deprecated_method(self):
            pass

        def mymethod(self, arg0, arg1, deprecated1=None, arg2='foo', deprecated2='bar', arg3='spam'):
            pass

    $ cat mymain.py
    from mymodule import deprecated_function, myfunction, MyClass

    deprecated_function()
    myfunction(0, 1, 'deprecated_arg1', deprecated_arg2=None)
    MyClass().deprecated_method()
    MyClass().mymethod(0, 1, deprecated1=None, deprecated2=None)

    $ pylint --load-plugins=deprecation_checker mymain.py
    ************* Module mymain
    mymain.py:3:0: W1505: Using deprecated method deprecated_function() (deprecated-method)
    mymain.py:4:0: W1511: Using deprecated argument deprecated_arg1 of method myfunction() (deprecated-argument)
    mymain.py:4:0: W1511: Using deprecated argument deprecated_arg2 of method myfunction() (deprecated-argument)
    mymain.py:5:0: W1505: Using deprecated method deprecated_method() (deprecated-method)
    mymain.py:6:0: W1511: Using deprecated argument deprecated1 of method mymethod() (deprecated-argument)
    mymain.py:6:0: W1511: Using deprecated argument deprecated2 of method mymethod() (deprecated-argument)

    ------------------------------------------------------------------
    Your code has been rated at 2.00/10 (previous run: 2.00/10, +0.00)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from pylint.checkers import BaseChecker, DeprecatedMixin

if TYPE_CHECKING:
    from pylint.lint import PyLinter


class DeprecationChecker(DeprecatedMixin, BaseChecker):
    """Class implementing deprecation checker."""

    # DeprecatedMixin class is Mixin class implementing logic for searching deprecated methods and functions.
    # The list of deprecated methods/functions is defined by the implementing class via
    # deprecated_methods callback. DeprecatedMixin class is overriding attributes of BaseChecker hence must
    # be specified *before* BaseChecker in list of base classes.

    # The name defines a custom section of the config for this checker.
    name = "deprecated"

    # Register messages emitted by the checker.
    msgs = {
        **DeprecatedMixin.DEPRECATED_METHOD_MESSAGE,
        **DeprecatedMixin.DEPRECATED_ARGUMENT_MESSAGE,
    }

    def deprecated_methods(self) -> set[str]:
        """Callback method called by DeprecatedMixin for every method/function found in the code.

        Returns:
            collections.abc.Container of deprecated function/method names.
        """
        return {"mymodule.deprecated_function", "mymodule.MyClass.deprecated_method"}

    def deprecated_arguments(self, method: str) -> tuple[tuple[int | None, str], ...]:
        """Callback returning the deprecated arguments of method/function.

        Returns:
            collections.abc.Iterable in form:
                ((POSITION1, PARAM1), (POSITION2: PARAM2) ...)
            where
                * POSITIONX - position of deprecated argument PARAMX in function definition.
                  If argument is keyword-only, POSITIONX should be None.
                * PARAMX - name of the deprecated argument.
        """
        if method == "mymodule.myfunction":
            # myfunction() has two deprecated arguments:
            # * deprecated_arg1 defined at 2nd position and
            # * deprecated_arg2 defined at 5th position.
            return ((2, "deprecated_arg1"), (5, "deprecated_arg2"))
        if method == "mymodule.MyClass.mymethod":
            # mymethod() has two deprecated arguments:
            # * deprecated1 defined at 2nd position and
            # * deprecated2 defined at 4th position.
            return ((2, "deprecated1"), (4, "deprecated2"))
        return ()


def register(linter: PyLinter) -> None:
    linter.register_checker(DeprecationChecker(linter))

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from pylint.testutils.checker_test_case import CheckerTestCase

if TYPE_CHECKING:
    from pylint.checkers.base_checker import BaseChecker


def set_config(**kwargs: Any) -> Callable:
    """Decorator for setting an option on the linter.

    Passing the args and kwargs back to the test function itself
    allows this decorator to be used on parametrized test cases.
    """

    def _wrapper(fun: Callable) -> Callable:
        @functools.wraps(fun)
        def _forward(
            self: BaseChecker | CheckerTestCase, *args: Any, **test_function_kwargs: Any
        ) -> None:
            """Set option via argparse."""
            for key, value in kwargs.items():
                self.linter.set_option(key, value)

            # Reopen checker in case, it may be interested in configuration change
            if isinstance(self, CheckerTestCase):
                self.checker.open()
            else:
                self.open()

            fun(self, *args, **test_function_kwargs)

        return _forward

    return _wrapper

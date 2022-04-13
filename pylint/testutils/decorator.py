# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import functools

from pylint.config.utils import _parse_rich_type_value
from pylint.testutils.checker_test_case import CheckerTestCase


def set_config(**kwargs):
    """Decorator for setting config values on a checker.

    Passing the args and kwargs back to the test function itself
    allows this decorator to be used on parametrized test cases.
    """

    def _wrapper(fun):
        @functools.wraps(fun)
        def _forward(self, *args, **test_function_kwargs):
            """Set option via argparse."""
            # pylint: disable-next=fixme
            # TODO: Revisit this decorator after all checkers have switched
            options = []
            for key, value in kwargs.items():
                options += [f"--{key.replace('_', '-')}", _parse_rich_type_value(value)]
            self.linter.namespace = self.linter._arg_parser.parse_known_args(
                options, self.linter.namespace
            )[0]

            if isinstance(self, CheckerTestCase):
                # reopen checker in case, it may be interested in configuration change
                self.checker.open()

            fun(self, *args, **test_function_kwargs)

        return _forward

    return _wrapper

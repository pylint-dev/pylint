# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

import functools

from pylint.testutils.checker_test_case import CheckerTestCase


def set_config(**kwargs):
    """Decorator for setting config values on a checker.

    Passing the args and kwargs back to the test function itself
    allows this decorator to be used on parametrized test cases.
    """

    def _wrapper(fun):
        @functools.wraps(fun)
        def _forward(self, *args, **test_function_kwargs):
            for key, value in kwargs.items():
                setattr(self.checker.config, key, value)
            if isinstance(self, CheckerTestCase):
                # reopen checker in case, it may be interested in configuration change
                self.checker.open()
            fun(self, *args, **test_function_kwargs)

        return _forward

    return _wrapper

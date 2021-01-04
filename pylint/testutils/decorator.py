# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import functools

from pylint.testutils.checker_test_case import CheckerTestCase


def set_config(**kwargs):
    """Decorator for setting config values on a checker."""

    def _wrapper(fun):
        @functools.wraps(fun)
        def _forward(self):
            for key, value in kwargs.items():
                setattr(self.checker.config, key, value)
            if isinstance(self, CheckerTestCase):
                # reopen checker in case, it may be interested in configuration change
                self.checker.open()
            fun(self)

        return _forward

    return _wrapper

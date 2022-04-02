# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import functools
import optparse  # pylint: disable=deprecated-module

from pylint import config
from pylint.lint import PyLinter
from pylint.testutils.checker_test_case import CheckerTestCase


def set_config(**kwargs):
    """Decorator for setting config values on a checker.

    Passing the args and kwargs back to the test function itself
    allows this decorator to be used on parametrized test cases.
    """

    def _wrapper(fun):
        @functools.wraps(fun)
        def _forward(self, *args, **test_function_kwargs):
            try:
                for key, value in kwargs.items():
                    self.checker.set_option(key.replace("_", "-"), value)
            except optparse.OptionError:
                # Check if option is one of the base options of the PyLinter class
                for key, value in kwargs.items():
                    try:
                        self.checker.set_option(
                            key.replace("_", "-"),
                            value,
                            optdict=dict(PyLinter.make_options())[
                                key.replace("_", "-")
                            ],
                        )
                    except KeyError:
                        # pylint: disable-next=fixme
                        # TODO: Find good way to double load checkers in unittests
                        # When options are used by multiple checkers we need to load both of them
                        # to be able to get an optdict
                        self.checker.set_option(
                            key.replace("_", "-"),
                            value,
                            optdict={},
                        )

            # Set option via argparse
            # pylint: disable-next=fixme
            # TODO: Revisit this decorator after all checkers have switched
            config_file_parser = config._ConfigurationFileParser(False, self.linter)
            options = []
            for key, value in kwargs.items():
                options += [
                    f"--{key.replace('_', '-')}",
                    config_file_parser._parse_toml_value(value),
                ]
            self.linter.namespace = self.linter._arg_parser.parse_known_args(
                options, self.linter.namespace
            )[0]

            if isinstance(self, CheckerTestCase):
                # reopen checker in case, it may be interested in configuration change
                self.checker.open()

            fun(self, *args, **test_function_kwargs)

        return _forward

    return _wrapper

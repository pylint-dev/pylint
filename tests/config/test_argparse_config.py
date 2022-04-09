# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Test for the (new) implementation of option parsing with argparse"""

import re
from os.path import abspath, dirname, join

import pytest

from pylint.lint import Run

HERE = abspath(dirname(__file__))
REGRTEST_DATA_DIR = join(HERE, "..", "regrtest_data")
EMPTY_MODULE = join(REGRTEST_DATA_DIR, "empty.py")
LOGGING_TEST = join(HERE, "data", "logging_format_interpolation_style.py")


class TestArgumentsManager:
    """Tests for the ArgumentsManager class"""

    base_run = Run([EMPTY_MODULE], exit=False)

    def test_namespace_creation(self) -> None:
        """Test that the linter object has a namespace attribute and that it is not empty"""

        assert self.base_run.linter.namespace
        assert self.base_run.linter.namespace._get_kwargs()


class TestArgparseOptionsProviderMixin:
    """Tests for the argparse implementation of OptionsProviderMixIn.

    The logger checker is used as an example checker for this implementation.
    """

    @staticmethod
    def test_logger_without_options() -> None:
        """Check that we raise messages when we do not supply any options."""
        with pytest.raises(SystemExit) as ex:
            Run([LOGGING_TEST])
        assert ex.value.code == 2

    @staticmethod
    def test_logger_commandline() -> None:
        """Check that we parse command-line options for the logging checker correctly."""
        with pytest.raises(SystemExit) as ex:
            Run([LOGGING_TEST, "--logging-format-style=new"])
        assert ex.value.code == 0

    @staticmethod
    def test_logger_rcfile() -> None:
        """Check that we parse the rcfile for the logging checker correctly."""
        with pytest.raises(SystemExit) as ex:
            Run([LOGGING_TEST, f"--rcfile={LOGGING_TEST.replace('.py', '.rc')}"])
        assert ex.value.code == 0


class TestDeprecationOptions:
    @staticmethod
    def test_new_names() -> None:
        """Check that we correctly emit DeprecationWarnings for deprecated options."""
        with pytest.raises(SystemExit) as ex:
            with pytest.warns(DeprecationWarning) as records:
                Run([EMPTY_MODULE, "--ignore-mixin-members=yes"])
            assert len(records) == 1
            assert "--ignore-mixin-members has been deprecated" in records[0]
        assert ex.value.code == 0

    @staticmethod
    def test_old_names() -> None:
        """Check that we correctly double assign old name options."""
        run = Run([EMPTY_MODULE, "--ignore=test,test_two"], exit=False)
        assert run.linter.namespace.ignore == ["test", "test_two"]
        assert run.linter.namespace.ignore == run.linter.namespace.black_list
        assert run.linter.namespace.ignore_patterns == [re.compile("^\\.#")]
        assert (
            run.linter.namespace.ignore_patterns == run.linter.namespace.black_list_re
        )

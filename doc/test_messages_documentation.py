# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Functional tests for the code examples in the messages' documentation."""

import sys

if sys.version_info[:2] > (3, 9):
    from collections import Counter
else:
    from collections import Counter as _Counter

    class Counter(_Counter):
        def total(self):
            return len(tuple(self.elements()))


from pathlib import Path
from typing import Counter as CounterType
from typing import List, Optional, TextIO, Tuple

import pytest

from pylint import checkers, config
from pylint.config.config_initialization import _config_initialization
from pylint.lint import PyLinter
from pylint.message.message import Message
from pylint.testutils.constants import _EXPECTED_RE
from pylint.testutils.reporter_for_tests import FunctionalTestReporter

MessageCounter = CounterType[Tuple[int, str]]


def get_functional_test_files_from_directory(input_dir: Path) -> List[Tuple[str, Path]]:
    """Get all functional tests in the input_dir.

    This also checks the formatting of related.rst files.
    """
    suite: List[Tuple[str, Path]] = []

    for subdirectory in input_dir.iterdir():
        for message_dir in subdirectory.iterdir():
            assert_msg = (
                f"{subdirectory}: '{message_dir.name}' is in the wrong "
                f"directory: it does not start with '{subdirectory.name}'"
            )
            assert message_dir.name.startswith(subdirectory.name), assert_msg
            if (message_dir / "good.py").exists():
                suite.append(
                    (message_dir.stem, message_dir / "good.py"),
                )
            if (message_dir / "bad.py").exists():
                suite.append(
                    (message_dir.stem, message_dir / "bad.py"),
                )
            if (message_dir / "related.rst").exists():
                with open(message_dir / "related.rst", encoding="utf-8") as file:
                    text = file.read()
                    assert text.startswith(
                        "-"
                    ), f"{message_dir / 'related.rst'} should be a list using '-'."
    return suite


TESTS_DIR = Path(__file__).parent.resolve() / "data" / "messages"
TESTS = get_functional_test_files_from_directory(TESTS_DIR)
TESTS_NAMES = [f"{t[0]}-{t[1].stem}" for t in TESTS]


class LintModuleTest:
    def __init__(self, test_file: Tuple[str, Path]) -> None:
        self._test_file = test_file

        _test_reporter = FunctionalTestReporter()

        self._linter = PyLinter()
        self._linter.config.persistent = 0
        checkers.initialize(self._linter)

        # Check if this message has a custom configuration file (e.g. for enabling optional checkers).
        # If not, use the default configuration.
        config_file: Optional[Path]
        if (test_file[1].parent / "pylintrc").exists():
            config_file = test_file[1].parent / "pylintrc"
        else:
            config_file = next(config.find_default_config_files(), None)

        _config_initialization(
            self._linter,
            args_list=[
                str(test_file[1]),
                "--disable=all",
                f"--enable={test_file[0]},astroid-error,fatal,syntax-error",
            ],
            reporter=_test_reporter,
            config_file=config_file,
        )

    def runTest(self) -> None:
        self._runTest()

    def is_good_test_file(self) -> bool:
        return self._test_file[1].name == "good.py"

    def is_bad_test_file(self) -> bool:
        return self._test_file[1].name == "bad.py"

    @staticmethod
    def get_expected_messages(stream: TextIO) -> MessageCounter:
        """Parse a file and get expected messages."""
        messages: MessageCounter = Counter()
        for i, line in enumerate(stream):
            match = _EXPECTED_RE.search(line)
            if match is None:
                continue

            line = match.group("line")
            if line is None:
                lineno = i + 1
            else:
                lineno = int(line)

            for msg_id in match.group("msgs").split(","):
                messages[lineno, msg_id.strip()] += 1
        return messages

    def _get_expected(self) -> MessageCounter:
        """Get the expected messages for a file."""
        with open(self._test_file[1], encoding="utf8") as f:
            expected_msgs = self.get_expected_messages(f)
        return expected_msgs

    def _get_actual(self) -> MessageCounter:
        """Get the actual messages after a run."""
        messages: List[Message] = self._linter.reporter.messages
        messages.sort(key=lambda m: (m.line, m.symbol, m.msg))
        received_msgs: MessageCounter = Counter()
        for msg in messages:
            received_msgs[msg.line, msg.symbol] += 1
        return received_msgs

    def _runTest(self) -> None:
        """Run the test and assert message differences."""
        self._linter.check([str(self._test_file[1])])
        expected_messages = self._get_expected()
        actual_messages = self._get_actual()
        if self.is_good_test_file():
            msg = "There should be no warning raised for 'goob.py'"
            assert actual_messages.total() == 0, msg  # type: ignore[attr-defined]
        if self.is_bad_test_file():
            msg = "There should be at least one warning raised for 'bad.py'"
            assert actual_messages.total() > 0, msg  # type: ignore[attr-defined]
        assert expected_messages == actual_messages


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_code_examples(test_file: Tuple[str, Path]) -> None:
    lint_test = LintModuleTest(test_file)
    lint_test.runTest()

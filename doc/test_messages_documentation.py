# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Functional tests for the code examples in the messages' documentation."""

from __future__ import annotations

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
from typing import TextIO, Tuple

import pytest

from pylint import checkers
from pylint.config.config_initialization import _config_initialization
from pylint.lint import PyLinter
from pylint.message.message import Message
from pylint.testutils.constants import _EXPECTED_RE
from pylint.testutils.reporter_for_tests import FunctionalTestReporter

MessageCounter = CounterType[Tuple[int, str]]


def get_functional_test_files_from_directory(input_dir: Path) -> list[tuple[str, Path]]:
    """Get all functional tests in the input_dir.

    This also checks the formatting of related.rst files.
    """
    suite: list[tuple[str, Path]] = []

    for subdirectory in input_dir.iterdir():
        for message_dir in subdirectory.iterdir():
            assert_msg = (
                f"{subdirectory}: '{message_dir.name}' is in the wrong "
                f"directory: it does not start with '{subdirectory.name}'"
            )
            assert message_dir.name.startswith(subdirectory.name), assert_msg
            _add_code_example_to_suite(message_dir, suite, "good")
            _add_code_example_to_suite(message_dir, suite, "bad")
            if (message_dir / "related.rst").exists():
                with open(message_dir / "related.rst", encoding="utf-8") as file:
                    text = file.read()
                    assert text.startswith(
                        "-"
                    ), f"{message_dir / 'related.rst'} should be a list using '-'."
    return suite


def _add_code_example_to_suite(
    message_dir: Path, suite: list[tuple[str, Path]], example_type: str
) -> None:
    """Code example files can either consist of a single file or a directory."""
    file = f"{example_type}.py"
    directory = f"{example_type}"
    if (message_dir / file).exists():
        suite.append(
            (message_dir.stem, message_dir / file),
        )
    elif (message_dir / directory).is_dir():
        dir_to_add = message_dir / directory
        len_to_add = len(list(dir_to_add.iterdir()))
        assert len_to_add > 1, (
            f"A directory of {example_type} files needs at least two files, "
            f"but only found one in {dir_to_add}."
        )
        suite.append(
            (message_dir.stem, dir_to_add),
        )


TESTS_DIR = Path(__file__).parent.resolve() / "data" / "messages"
TESTS = get_functional_test_files_from_directory(TESTS_DIR)
TESTS_NAMES = [f"{t[0]}-{t[1].stem}" for t in TESTS]


class LintModuleTest:
    def __init__(self, test_file: tuple[str, Path]) -> None:
        self._test_file = test_file

        _test_reporter = FunctionalTestReporter()

        self._linter = PyLinter()
        self._linter.config.persistent = 0
        checkers.initialize(self._linter)

        # Check if this message has a custom configuration file (e.g. for enabling optional checkers).
        # If not, use the default configuration.
        config_file: Path | None
        msgid, full_path = test_file
        pylintrc = full_path.parent / "pylintrc"
        config_file = pylintrc if pylintrc.exists() else None
        print(f"Config file used: {config_file}")
        args = [
            str(full_path),
            "--disable=all",
            f"--enable=F,{msgid},astroid-error,syntax-error",
        ]
        print(f"Command used:\npylint {' '.join(args)}")
        _config_initialization(
            self._linter,
            args_list=args,
            reporter=_test_reporter,
            config_file=config_file,
        )

    def runTest(self) -> None:
        self._runTest()

    def is_good_test(self) -> bool:
        return self._test_file[1].stem == "good"

    def is_bad_test(self) -> bool:
        return self._test_file[1].stem == "bad"

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
            elif line.startswith("+") or line.startswith("-"):
                lineno = i + 1 + int(line)
            else:
                lineno = int(line)

            for msg_id in match.group("msgs").split(","):
                messages[lineno, msg_id.strip()] += 1
        return messages

    def _get_expected(self) -> dict[Path, MessageCounter]:
        """Get the expected messages for a file or directory."""
        expected_msgs: dict[Path, MessageCounter] = {}
        if self._test_file[1].is_dir():
            for _i, test_file in enumerate(self._test_file[1].iterdir()):
                expected_msgs[test_file] = Counter()
                with open(test_file, encoding="utf8") as f:
                    expected_msgs[test_file] += self.get_expected_messages(f)
        else:
            expected_msgs[self._test_file[1]] = Counter()
            with open(self._test_file[1], encoding="utf8") as f:
                expected_msgs[self._test_file[1]] += self.get_expected_messages(f)
        return expected_msgs

    def _get_actual(self) -> MessageCounter:
        """Get the actual messages after a run."""
        messages: list[Message] = self._linter.reporter.messages
        str_messages = "\n- ".join([str(m) for m in messages])
        print(f"Actual messages raised:\n- {str_messages}")
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
        if self.is_good_test():
            assert actual_messages.total() == 0, self.assert_message_good(
                actual_messages
            )
        if self.is_bad_test():
            msg = "There should be at least one warning raised for 'bad' examples."
            assert actual_messages.total() > 0, msg
        all_files_counter: Counter[tuple[int, str]] = Counter()
        for expected_message in expected_messages.values():
            all_files_counter += expected_message
        assert all_files_counter == actual_messages

    def assert_message_good(self, actual_messages: MessageCounter) -> str:
        if not actual_messages:
            return ""
        messages = "\n- ".join(f"{v} (l. {i})" for i, v in actual_messages)
        msg = f"""There should be no warning raised for 'good.py' but these messages were raised:
- {messages}

See:

"""

        def create_representation_of_issue(
            file_path: Path | str,
            inner_actual_messages: Counter[tuple[int, str]],
            certainty: str,
        ) -> str:
            with open(file_path) as f:
                lines = [line[:-1] for line in f.readlines()]
            for line_index, value in inner_actual_messages:
                if line_index - 1 >= len(lines):
                    # If the line does not exist, we know that the message
                    # can't be emitted from this file
                    return ""
                comment = f"  # <-- /!\\ unexpected '{value}' {certainty}/!\\"
                lines[line_index - 1] += comment
            return "\n".join(lines)

        good = self._test_file[1]
        if good.is_file():
            return f"{msg}{create_representation_of_issue(good, actual_messages, '')}"
        else:
            representations: dict[str, str] = {}
            good_files = [str(g) for g in good.iterdir()]
            for file_ in good_files:
                file_representation = create_representation_of_issue(
                    file_,
                    actual_messages,
                    certainty="(maybe in another file ?)"
                    if len(good_files) > 1
                    else "",
                )
                if file_representation:
                    representations[file_] = file_representation
            if len(representations) == 1:
                return next(iter(representations.values()))
            else:
                separator = f"\n{'_' * 80}\n"
                str_files = ""
                for file_path, representation in representations.items():
                    str_files += f"{separator}{file_path}{separator}{representation}\n"
                return f"{msg}{separator}{str_files}{separator}\nOnly one file is a problem!"


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_code_examples(test_file: tuple[str, Path]) -> None:
    lint_test = LintModuleTest(test_file)
    lint_test.runTest()

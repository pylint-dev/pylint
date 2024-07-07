# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Functional tests for the code examples in the messages' documentation."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import TextIO

import pytest

from pylint import checkers
from pylint.config.config_initialization import _config_initialization
from pylint.lint import PyLinter
from pylint.message.message import Message
from pylint.testutils.constants import _EXPECTED_RE
from pylint.testutils.reporter_for_tests import FunctionalTestReporter

MessageCounter = Counter[tuple[int, str]]


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
    def __init__(
        self, test_file: tuple[str, Path], multiple_file_messages: list[str]
    ) -> None:
        self._test_file = test_file
        self._multiple_file_messages = multiple_file_messages

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
            elif line.startswith(("+", "-")):
                lineno = i + 1 + int(line)
            else:
                lineno = int(line)

            for msg_id in match.group("msgs").split(","):
                messages[lineno, msg_id.strip()] += 1
        return messages

    def _get_expected(self) -> MessageCounter:
        """Get the expected messages for a file or directory."""
        expected_msgs: MessageCounter = Counter()
        if self._test_file[1].is_dir():
            for test_file in self._test_file[1].iterdir():
                with open(test_file, encoding="utf8") as f:
                    expected_msgs += self.get_expected_messages(f)
        else:
            with open(self._test_file[1], encoding="utf8") as f:
                expected_msgs += self.get_expected_messages(f)
        return expected_msgs

    def _get_actual(self, messages: list[Message]) -> MessageCounter:
        """Get the actual messages after a run."""
        messages.sort(key=lambda m: (m.line, m.symbol, m.msg))
        received_msgs: MessageCounter = Counter()
        for msg in messages:
            received_msgs[msg.line, msg.symbol] += 1
        return received_msgs

    def _runTest(self) -> None:
        """Run the test and assert message differences."""
        self._linter.check([str(self._test_file[1])])
        expected_messages = self._get_expected()
        actual_messages_raw = self._linter.reporter.messages
        if self.is_good_test():
            assert not actual_messages_raw, self.assert_message_good(
                actual_messages_raw
            )
        if self.is_bad_test():
            bad_files = [(self._test_file[1])]
            if self._test_file[1].is_dir() and not self.is_multifile_example():
                bad_files = list(self._test_file[1].iterdir())
            assert len(actual_messages_raw) >= len(bad_files), self.assert_message_bad(
                bad_files, actual_messages_raw
            )
        assert expected_messages == self._get_actual(actual_messages_raw)

    def assert_message_good(self, messages: list[Message]) -> str:
        good = self._test_file[1]
        msg = f"There should be no warning raised for '{good}' but these messages were raised:\n"
        file_representations = {}
        for message in messages:
            if message.path not in file_representations:
                with open(message.path) as f:
                    file_representations[message.path] = [
                        line[:-1] for line in f.readlines()
                    ]
            file_representations[message.path][
                message.line - 1
            ] += f"  # <-- /!\\ unexpected '{message.symbol}' /!\\"
        for path, representation in file_representations.items():
            file_representation = "\n".join(representation)
            msg += f"\n\n\nIn {path}:\n\n{file_representation}\n"
        return msg

    def is_multifile_example(self) -> bool:
        """Multiple file example do not need to have one warning for each bad file."""
        return self._test_file[0] in self._multiple_file_messages

    def assert_message_bad(self, bad_files: list[Path], messages: list[Message]) -> str:
        each = "each file in " if len(bad_files) > 1 else ""
        msg = (
            f"There should be at least one warning raised for "
            f"{each}'{self._test_file[1]}' ({len(bad_files)} total)\n"
        )
        raised_files: set[Path] = set()
        for message in messages:
            raised_files.add(Path(message.path).absolute())
        missing_files = set(bad_files) - raised_files
        for missing_file in missing_files:
            msg += f"- Missing warning in {missing_file}\n"
        if messages:
            msg += f"'{messages[0].symbol}' might need to be added in 'known_multiple_file_messages'.\n\n"
        return msg


@pytest.mark.parametrize("test_file", TESTS, ids=TESTS_NAMES)
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_code_examples(test_file: tuple[str, Path]) -> None:
    known_multiple_file_messages = ["cyclic-import", "duplicate-code"]
    lint_test = LintModuleTest(test_file, known_multiple_file_messages)
    lint_test.runTest()

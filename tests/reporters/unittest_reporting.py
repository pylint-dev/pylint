# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=redefined-outer-name

from __future__ import annotations

import warnings
from contextlib import redirect_stdout
from io import StringIO
from json import dumps
from pathlib import Path
from typing import TYPE_CHECKING, TextIO

import pytest

from pylint import checkers
from pylint.interfaces import HIGH
from pylint.lint import PyLinter
from pylint.message.message import Message
from pylint.reporters import BaseReporter, MultiReporter
from pylint.reporters.text import ParseableTextReporter, TextReporter
from pylint.typing import FileItem, MessageLocationTuple

if TYPE_CHECKING:
    from pylint.reporters.ureports.nodes import Section


@pytest.fixture(scope="module")
def reporter() -> type[TextReporter]:
    return TextReporter


@pytest.fixture(scope="module")
def disable() -> list[str]:
    return ["I"]


def test_template_option(linter: PyLinter) -> None:
    output = StringIO()
    linter.reporter.out = output
    linter.config.msg_template = "{msg_id}:{line:03d}"
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message("line-too-long", line=2, args=(3, 4))
    assert output.getvalue() == "************* Module 0123\nC0301:001\nC0301:002\n"


def test_template_option_default(linter: PyLinter) -> None:
    """Test the default msg-template setting."""
    output = StringIO()
    linter.reporter.out = output
    linter.open()
    linter.set_current_module("my_module")
    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message("line-too-long", line=2, args=(3, 4))

    out_lines = output.getvalue().split("\n")
    assert out_lines[1] == "my_module:1:0: C0301: Line too long (1/2) (line-too-long)"
    assert out_lines[2] == "my_module:2:0: C0301: Line too long (3/4) (line-too-long)"


def test_template_option_end_line(linter: PyLinter) -> None:
    """Test the msg-template option with end_line and end_column."""
    output = StringIO()
    linter.reporter.out = output
    linter.config.msg_template = (
        "{path}:{line}:{column}:{end_line}:{end_column}: {msg_id}: {msg} ({symbol})"
    )
    linter.open()
    linter.set_current_module("my_mod")
    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message(
        "line-too-long", line=2, end_lineno=2, end_col_offset=4, args=(3, 4)
    )

    out_lines = output.getvalue().split("\n")
    assert out_lines[1] == "my_mod:1:0::: C0301: Line too long (1/2) (line-too-long)"
    assert out_lines[2] == "my_mod:2:0:2:4: C0301: Line too long (3/4) (line-too-long)"


def test_template_option_non_existing(linter: PyLinter) -> None:
    """Test the msg-template option with non-existent options.
    This makes sure that this option remains backwards compatible as new
    parameters do not break on previous versions.
    """
    output = StringIO()
    linter.reporter.out = output
    linter.config.msg_template = "{path}:{line}:{categ}:({a_second_new_option:03d})"
    linter.open()
    with pytest.warns(UserWarning) as records:
        linter.set_current_module("my_mod")
        assert len(records) == 2
        assert "Don't recognize the argument 'categ'" in records[0].message.args[0]
    assert (
        "Don't recognize the argument 'a_second_new_option'"
        in records[1].message.args[0]
    )

    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message(
        "line-too-long", line=2, end_lineno=2, end_col_offset=4, args=(3, 4)
    )

    out_lines = output.getvalue().split("\n")
    assert out_lines[1] == "my_mod:1::()"
    assert out_lines[2] == "my_mod:2::()"


def test_template_option_with_header(linter: PyLinter) -> None:
    output = StringIO()
    linter.reporter.out = output
    linter.config.msg_template = '{{ "Category": "{category}" }}'
    linter.open()
    linter.set_current_module("my_mod")

    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message(
        "line-too-long", line=2, end_lineno=2, end_col_offset=4, args=(3, 4)
    )

    out_lines = output.getvalue().split("\n")
    assert out_lines[1] == '{ "Category": "convention" }'
    assert out_lines[2] == '{ "Category": "convention" }'


def test_parseable_output_deprecated() -> None:
    with warnings.catch_warnings(record=True) as cm:
        warnings.simplefilter("always")
        ParseableTextReporter()

    assert len(cm) == 1
    assert isinstance(cm[0].message, DeprecationWarning)


def test_parseable_output_regression() -> None:
    output = StringIO()
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("ignore", category=DeprecationWarning)
        linter = PyLinter(reporter=ParseableTextReporter())

    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.reporter.out = output
    linter.set_option("output-format", "parseable")
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))
    assert (
        output.getvalue() == "************* Module 0123\n"
        "0123:1: [C0301(line-too-long), ] "
        "Line too long (1/2)\n"
    )


class NopReporter(BaseReporter):
    name = "nop-reporter"
    extension = ""

    def __init__(self, output: TextIO | None = None) -> None:
        super().__init__(output)
        print("A NopReporter was initialized.", file=self.out)

    def writeln(self, string: str = "") -> None:
        pass

    def _display(self, layout: Section) -> None:
        pass


def test_multi_format_output(tmp_path: Path) -> None:
    text = StringIO(newline=None)
    json = tmp_path / "somefile.json"

    source_file = tmp_path / "somemodule.py"
    source_file.write_text('NOT_EMPTY = "This module is not empty"\n')
    dumps(str(source_file))

    nop_format = NopReporter.__module__ + "." + NopReporter.__name__
    formats = ",".join(["json2:" + str(json), "text", nop_format])

    with redirect_stdout(text):
        linter = PyLinter()
        linter.load_default_plugins()
        linter.set_option("persistent", False)
        linter.set_option("reports", True)
        linter.set_option("score", True)
        linter.set_option("score", True)
        linter.set_option("output-format", formats)

        assert linter.reporter.linter is linter
        with pytest.raises(NotImplementedError):
            linter.reporter.out = text

        linter.open()
        linter.check_single_file_item(
            FileItem("somemodule", str(source_file), "somemodule")
        )
        linter.add_message("line-too-long", line=1, args=(1, 2))
        linter.generate_reports()
        linter.reporter.writeln("direct output")

        # Ensure the output files are flushed and closed
        assert isinstance(linter.reporter, MultiReporter)
        linter.reporter.close_output_files()
        del linter.reporter

    with open(json, encoding="utf-8") as f:
        assert '"messageId": "C0114"' in f.read()

    assert (
        text.getvalue() == "A NopReporter was initialized.\n"
        "************* Module somemodule\n"
        f"{source_file}:1:0: C0114: Missing module docstring (missing-module-docstring)\n"
        f"{source_file}:1:0: C0301: Line too long (1/2) (line-too-long)\n"
        "\n"
        "\n"
        "Report\n"
        "======\n"
        "1 statements analysed.\n"
        "\n"
        "Statistics by type\n"
        "------------------\n"
        "\n"
        "+---------+-------+-----------+-----------+------------+---------+\n"
        "|type     |number |old number |difference |%documented |%badname |\n"
        "+=========+=======+===========+===========+============+=========+\n"
        "|module   |1      |NC         |NC         |0.00        |0.00     |\n"
        "+---------+-------+-----------+-----------+------------+---------+\n"
        "|class    |0      |NC         |NC         |0           |0        |\n"
        "+---------+-------+-----------+-----------+------------+---------+\n"
        "|method   |0      |NC         |NC         |0           |0        |\n"
        "+---------+-------+-----------+-----------+------------+---------+\n"
        "|function |0      |NC         |NC         |0           |0        |\n"
        "+---------+-------+-----------+-----------+------------+---------+\n"
        "\n"
        "\n"
        "\n"
        "3 lines have been analyzed\n"
        "\n"
        "Raw metrics\n"
        "-----------\n"
        "\n"
        "+----------+-------+------+---------+-----------+\n"
        "|type      |number |%     |previous |difference |\n"
        "+==========+=======+======+=========+===========+\n"
        "|code      |2      |66.67 |NC       |NC         |\n"
        "+----------+-------+------+---------+-----------+\n"
        "|docstring |0      |0.00  |NC       |NC         |\n"
        "+----------+-------+------+---------+-----------+\n"
        "|comment   |0      |0.00  |NC       |NC         |\n"
        "+----------+-------+------+---------+-----------+\n"
        "|empty     |1      |33.33 |NC       |NC         |\n"
        "+----------+-------+------+---------+-----------+\n"
        "\n"
        "\n"
        "\n"
        "Duplication\n"
        "-----------\n"
        "\n"
        "+-------------------------+------+---------+-----------+\n"
        "|                         |now   |previous |difference |\n"
        "+=========================+======+=========+===========+\n"
        "|nb duplicated lines      |0     |NC       |NC         |\n"
        "+-------------------------+------+---------+-----------+\n"
        "|percent duplicated lines |0.000 |NC       |NC         |\n"
        "+-------------------------+------+---------+-----------+\n"
        "\n"
        "\n"
        "\n"
        "Messages by category\n"
        "--------------------\n"
        "\n"
        "+-----------+-------+---------+-----------+\n"
        "|type       |number |previous |difference |\n"
        "+===========+=======+=========+===========+\n"
        "|convention |2      |NC       |NC         |\n"
        "+-----------+-------+---------+-----------+\n"
        "|refactor   |0      |NC       |NC         |\n"
        "+-----------+-------+---------+-----------+\n"
        "|warning    |0      |NC       |NC         |\n"
        "+-----------+-------+---------+-----------+\n"
        "|error      |0      |NC       |NC         |\n"
        "+-----------+-------+---------+-----------+\n"
        "\n"
        "\n"
        "\n"
        "Messages\n"
        "--------\n"
        "\n"
        "+-------------------------+------------+\n"
        "|message id               |occurrences |\n"
        "+=========================+============+\n"
        "|missing-module-docstring |1           |\n"
        "+-------------------------+------------+\n"
        "|line-too-long            |1           |\n"
        "+-------------------------+------------+\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "-----------------------------------\n"
        "Your code has been rated at 0.00/10\n"
        "\n"
        "direct output\n"
    )


def test_multi_reporter_independant_messages() -> None:
    """Messages should not be modified by multiple reporters."""
    check_message = "Not modified"

    class ReporterModify(BaseReporter):
        def handle_message(self, msg: Message) -> None:
            msg.msg = "Modified message"

        def writeln(self, string: str = "") -> None:
            pass

        def _display(self, layout: Section) -> None:
            pass

    class ReporterCheck(BaseReporter):
        def handle_message(self, msg: Message) -> None:
            assert (
                msg.msg == check_message
            ), "Message object should not be changed by other reporters."

        def writeln(self, string: str = "") -> None:
            pass

        def _display(self, layout: Section) -> None:
            pass

    multi_reporter = MultiReporter([ReporterModify(), ReporterCheck()], lambda: None)

    message = Message(
        symbol="missing-docstring",
        msg_id="C0123",
        location=MessageLocationTuple("abspath", "path", "module", "obj", 1, 2, 1, 3),
        msg=check_message,
        confidence=HIGH,
    )

    multi_reporter.handle_message(message)

    assert (
        message.msg == check_message
    ), "Message object should not be changed by reporters."


def test_display_results_is_renamed() -> None:
    class CustomReporter(TextReporter):
        def _display(self, layout: Section) -> None:
            return None

    reporter = CustomReporter()
    with pytest.raises(AttributeError) as exc:
        # pylint: disable=no-member
        reporter.display_results()  # type: ignore[attr-defined]
    assert "no attribute 'display_results'" in str(exc)

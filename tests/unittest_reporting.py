# Copyright (c) 2013-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2014-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2014 Calin Don <calin.don@gmail.com>
# Copyright (c) 2014 Google, Inc.
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016-2017 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 ruro <ruro.ruro@ya.ru>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
# pylint: disable=redefined-outer-name

import warnings
from contextlib import redirect_stdout
from io import StringIO
from json import dumps

import pytest

from pylint import checkers
from pylint.interfaces import IReporter
from pylint.lint import PyLinter
from pylint.reporters import BaseReporter
from pylint.reporters.text import ParseableTextReporter, TextReporter


@pytest.fixture(scope="module")
def reporter():
    return TextReporter


@pytest.fixture(scope="module")
def disable():
    return ["I"]


def test_template_option(linter):
    output = StringIO()
    linter.reporter.set_output(output)
    linter.set_option("msg-template", "{msg_id}:{line:03d}")
    linter.open()
    linter.set_current_module("0123")
    linter.add_message("C0301", line=1, args=(1, 2))
    linter.add_message("line-too-long", line=2, args=(3, 4))
    assert output.getvalue() == "************* Module 0123\nC0301:001\nC0301:002\n"


def test_parseable_output_deprecated():
    with warnings.catch_warnings(record=True) as cm:
        warnings.simplefilter("always")
        ParseableTextReporter()

    assert len(cm) == 1
    assert isinstance(cm[0].message, DeprecationWarning)


def test_parseable_output_regression():
    output = StringIO()
    with warnings.catch_warnings(record=True):
        linter = PyLinter(reporter=ParseableTextReporter())

    checkers.initialize(linter)
    linter.config.persistent = 0
    linter.reporter.set_output(output)
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
    __implements__ = IReporter
    name = "nop-reporter"
    extension = ""

    def __init__(self, output=None):
        super().__init__(output)
        print("A NopReporter was initialized.", file=self.out)

    def writeln(self, string=""):
        pass

    def _display(self, layout):
        pass


def test_multi_format_output(tmp_path):
    text = StringIO(newline=None)
    json = tmp_path / "somefile.json"

    source_file = tmp_path / "somemodule.py"
    source_file.write_text('NOT_EMPTY = "This module is not empty"\n')
    escaped_source_file = dumps(str(source_file))

    nop_format = NopReporter.__module__ + "." + NopReporter.__name__
    formats = ",".join(["json:" + str(json), "text", nop_format])

    with redirect_stdout(text):
        linter = PyLinter()
        linter.set_option("persistent", False)
        linter.set_option("output-format", formats)
        linter.set_option("reports", True)
        linter.set_option("score", True)
        linter.load_default_plugins()

        assert linter.reporter.linter is linter
        with pytest.raises(NotImplementedError):
            linter.reporter.set_output(text)

        linter.open()
        linter.check_single_file("somemodule", source_file, "somemodule")
        linter.add_message("line-too-long", line=1, args=(1, 2))
        linter.generate_reports()
        linter.reporter.writeln("direct output")

        # Ensure the output files are flushed and closed
        linter.reporter.close_output_files()
        del linter.reporter

    with open(json) as f:
        assert (
            f.read() == "[\n"
            "    {\n"
            '        "type": "convention",\n'
            '        "module": "somemodule",\n'
            '        "obj": "",\n'
            '        "line": 1,\n'
            '        "column": 0,\n'
            f'        "path": {escaped_source_file},\n'
            '        "symbol": "missing-module-docstring",\n'
            '        "message": "Missing module docstring",\n'
            '        "message-id": "C0114"\n'
            "    },\n"
            "    {\n"
            '        "type": "convention",\n'
            '        "module": "somemodule",\n'
            '        "obj": "",\n'
            '        "line": 1,\n'
            '        "column": 0,\n'
            f'        "path": {escaped_source_file},\n'
            '        "symbol": "line-too-long",\n'
            '        "message": "Line too long (1/2)",\n'
            '        "message-id": "C0301"\n'
            "    }\n"
            "]\n"
            "direct output\n"
        )

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
        "-------------------------------------\n"
        "Your code has been rated at -10.00/10\n"
        "\n"
        "direct output\n"
    )


def test_display_results_is_renamed():
    class CustomReporter(TextReporter):
        def _display(self, layout):
            return None

    reporter = CustomReporter()
    with pytest.raises(AttributeError) as exc:
        # pylint: disable=no-member
        reporter.display_results()
    assert "no attribute 'display_results'" in str(exc)

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from pathlib import Path
from textwrap import dedent

import astroid
import pytest

from pylint.checkers import base
from pylint.interfaces import HIGH
from pylint.lint import PyLinter
from pylint.testutils import CheckerTestCase, GenericTestReporter, MessageTest


@pytest.mark.parametrize("jobs", [1, 2])
@pytest.mark.parametrize(
    "filenames",
    [
        ("attribute_consumer.py",),
        ("attribute_definitions.py",),
        ("attribute_consumer.py", "attribute_definitions.py"),
        ("attribute_definitions.py", "attribute_consumer.py"),
    ],
)
def test_instance_attribute_names_across_modules(
    linter: PyLinter,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    jobs: int,
    filenames: tuple[str, ...],
) -> None:
    definitions = tmp_path / "attribute_definitions.py"
    definitions.write_text(
        dedent(
            """\
        from typing import Final

        class Record:
            FieldName = ""

            def __init__(self):
                self.LocalName = ""
                self.SuppressedName = ""  # pylint: disable=invalid-name
                self.FINAL_VALUE: Final[str] = ""
                self.foo = ""

        class Derived(Record):
            def __init__(self):
                self.LocalName = ""
        """
        ),
        encoding="utf-8",
    )
    (tmp_path / "attribute_consumer.py").write_text(
        dedent(
            """\
        from attribute_definitions import Record

        record = Record()
        record.FieldName = "value"
        record.NewName = "value"
        record.LocalName = "value"
        record.SuppressedName = "value"
        record.bar = "value"
        """
        ),
        encoding="utf-8",
    )
    monkeypatch.syspath_prepend(tmp_path)
    astroid.MANAGER.clear_cache()
    reporter = GenericTestReporter()
    linter.set_reporter(reporter)
    linter.disable("all")
    linter.enable("invalid-name")
    linter.enable("disallowed-name")
    linter.enable("useless-suppression")
    linter.set_option("class-attribute-naming-style", "any")
    linter.set_option("jobs", jobs)

    linter.check([str(tmp_path / filename) for filename in filenames])

    expected = (
        [
            ("invalid-name", "attribute_definitions", 7),
            ("disallowed-name", "attribute_definitions", 10),
        ]
        if "attribute_definitions.py" in filenames
        else []
    )
    assert [(m.symbol, m.module, m.line) for m in reporter.messages] == expected


class TestInstanceAttributeNames(CheckerTestCase):
    CHECKER_CLASS = base.NameChecker

    def test_local_assignment_after_foreign_assignment(self) -> None:
        module = astroid.parse(
            """\
class Record:
    def __init__(self):
        self.BadName = ""
"""
        )
        record = module["Record"]
        assignment = record.instance_attrs["BadName"][0]
        foreign_assignment = astroid.extract_node('record.BadName = "value"').targets[0]
        record.instance_attrs["BadName"].insert(0, foreign_assignment)

        with self.assertAddsMessages(
            MessageTest(
                "invalid-name",
                node=assignment,
                args=("Attribute", "BadName", "snake_case naming style"),
                confidence=HIGH,
            ),
            ignore_position=True,
        ):
            self.checker.visit_classdef(record)

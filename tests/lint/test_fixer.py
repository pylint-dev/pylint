# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Tests for the data model of fixes and for applying them to source code."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import astroid
import pytest
from astroid import nodes

from pylint.checkers import BaseChecker
from pylint.exceptions import InvalidMessageError
from pylint.interfaces import UNDEFINED
from pylint.lint import PyLinter
from pylint.lint.fixer import apply_fixes, read_source, write_source
from pylint.message import Applicability, Edit, Fix, source_segment, source_tokens
from pylint.reporters import CollectingReporter

SAFE = {Applicability.SAFE}
ALL = {Applicability.SAFE, Applicability.UNSAFE}


def _fix(
    *edits: Edit | None,
    applicability: Applicability = Applicability.SAFE,
    name: str = "fix",
) -> Fix:
    fix = Fix.create(name, *edits, applicability=applicability)
    assert fix is not None
    return fix


def test_edit_must_not_end_before_it_starts() -> None:
    with pytest.raises(ValueError, match="ends before it starts"):
        Edit(2, 0, 1, 0, "")


def test_fix_edits_must_not_overlap() -> None:
    with pytest.raises(ValueError, match="overlap"):
        _fix(Edit(1, 0, 1, 5, "a"), Edit(1, 3, 1, 8, "b"))
    with pytest.raises(ValueError, match="at least one edit"):
        Fix("empty", ())


def test_fix_create_returns_none_when_an_edit_is_missing() -> None:
    assert Fix.create("no edit") is None
    assert Fix.create("missing", Edit(1, 0, 1, 1, "a"), None) is None
    fix = Fix.create("ok", Edit(1, 0, 1, 1, "a"), applicability=Applicability.SAFE)
    assert fix == _fix(Edit(1, 0, 1, 1, "a"), name="ok")


def test_apply_replacement_deletion_and_insertion() -> None:
    source = "a = 1\nb = 2 + 0\n"
    result = apply_fixes(
        source,
        [
            _fix(Edit(1, 4, 1, 5, "10")),
            _fix(Edit(2, 0, 2, 0, "# hello\n")),
            _fix(Edit(2, 5, 2, 9, "")),
        ],
        SAFE,
    )
    assert result.source == "a = 10\n# hello\nb = 2\n"
    assert result.syntax_error is None


def test_fixes_producing_invalid_code_are_reverted() -> None:
    source = "a = 1\n"
    result = apply_fixes(source, [_fix(Edit(1, 4, 1, 5, ""))], SAFE)
    assert result.syntax_error is not None
    assert result.source == source


def test_apply_multiline_edit() -> None:
    source = "x = (\n    1,\n    2,\n)\ny = 3\n"
    result = apply_fixes(source, [_fix(Edit(1, 4, 4, 1, "(1, 2)"))], SAFE)
    assert result.source == "x = (1, 2)\ny = 3\n"


def test_overlapping_fixes_first_one_wins() -> None:
    first = _fix(Edit(1, 4, 1, 9, "first"), name="first")
    second = _fix(Edit(1, 6, 1, 12, "second"), name="second")
    result = apply_fixes("x = 123456789\n", [second, first], SAFE)
    assert result.applied == [first]
    assert result.conflicting == [second]
    assert result.source == "x = first6789\n"


def test_touching_fixes_conflict() -> None:
    insert = _fix(Edit(1, 4, 1, 4, "-"), name="insert")
    other_insert = _fix(Edit(1, 4, 1, 4, "+"), name="other insert")
    result = apply_fixes("x = 1\n", [insert, other_insert], SAFE)
    assert result.applied == [insert]
    assert result.conflicting == [other_insert]


def test_identical_edits_are_applied_once() -> None:
    shared_import = Edit(1, 0, 1, 0, "import os\n")
    first = _fix(shared_import, Edit(2, 0, 2, 1, "os.sep"), name="first")
    second = _fix(shared_import, Edit(3, 0, 3, 1, "os.sep"), name="second")
    result = apply_fixes("x = 1\na\nb\n", [first, second], SAFE)
    assert result.applied == [first, second]
    assert result.source == "import os\nx = 1\nos.sep\nos.sep\n"


def test_a_fix_is_applied_as_a_whole_or_not_at_all() -> None:
    blocking = _fix(Edit(2, 0, 2, 1, "c"), name="blocking")
    two_edits = _fix(Edit(1, 0, 1, 1, "y"), Edit(2, 0, 2, 1, "z"), name="two edits")
    result = apply_fixes("x\na\n", [blocking, two_edits], SAFE)
    assert result.applied == [two_edits]
    assert result.conflicting == [blocking]
    assert result.source == "y\nz\n"


def test_applicability_is_respected() -> None:
    unsafe = _fix(Edit(1, 0, 1, 1, "y"), applicability=Applicability.UNSAFE)
    display_only = _fix(Edit(1, 0, 1, 1, "z"), applicability=Applicability.DISPLAY_ONLY)
    result = apply_fixes("x\n", [unsafe, display_only], SAFE)
    assert result.not_allowed == [unsafe, display_only]
    assert result.source == "x\n"
    result = apply_fixes("x\n", [unsafe, display_only], ALL)
    assert result.applied == [unsafe]
    assert result.source == "y\n"


def test_safe_fix_removing_a_comment_is_unsafe() -> None:
    source = "x = (1  # one\n     + 2)\n"
    fix = _fix(Edit(1, 4, 2, 9, "3"))
    assert apply_fixes(source, [fix], SAFE).not_allowed == [fix]
    assert apply_fixes(source, [fix], ALL).source == "x = 3\n"
    # A comment next to the edit is kept, the fix stays safe
    result = apply_fixes("x = 1  # one\n", [_fix(Edit(1, 4, 1, 5, "2"))], SAFE)
    assert result.source == "x = 2  # one\n"


def test_columns_are_utf8_byte_offsets() -> None:
    source = 'x = "pomme é"; y = 1\n'
    module = astroid.parse(source)
    number = module.body[1].value
    # 'é' is two bytes long in UTF-8
    assert number.col_offset == 20
    edit = Edit.replace(number, "2")
    assert apply_fixes(source, [_fix(edit)], SAFE).source == 'x = "pomme é"; y = 2\n'
    assert Edit.from_character_columns(
        1, 19, 1, 20, "2", source_lines=source.splitlines(keepends=True)
    ) == Edit(1, 20, 1, 21, "2")


def test_edit_at_the_end_of_a_file_without_newline() -> None:
    result = apply_fixes("x = 1", [_fix(Edit(1, 5, 1, 5, "\n"))], SAFE)
    assert result.source == "x = 1\n"


def test_edit_helpers_from_nodes() -> None:
    module = astroid.parse("x = (apple  +  1)\n")
    binop = module.body[0].value
    assert Edit.replace(binop, "2") == Edit(1, 5, 1, 16, "2", module.file)
    assert Edit.delete(binop) == Edit(1, 5, 1, 16, "", module.file)
    assert Edit.insert_before(binop, "-") == Edit(1, 5, 1, 5, "-", module.file)
    assert Edit.insert_after(binop, "-") == Edit(1, 16, 1, 16, "-", module.file)
    synthetic = nodes.Const(1)
    assert Edit.replace(synthetic, "2") is None
    assert Edit.insert_before(synthetic, "2") is None
    assert Edit.insert_after(synthetic, "2") is None


def test_source_segment_keeps_the_original_code(tmp_path: Path) -> None:
    source = "x = double((apple  +  1))\ny = ['a',  # comment\n     \"b\"]\n"
    module = astroid.parse(source)
    call = module.body[0].value
    # The parentheses around the argument are not part of the node
    assert source_segment(call.args[0]) == "apple  +  1"
    assert call.args[0].as_string() == "apple + 1"
    assert source_segment(module.body[1].value) == "['a',  # comment\n     \"b\"]"
    assert source_segment(nodes.Const(1)) is None

    path = tmp_path / "latin.py"
    path.write_bytes("# -*- coding: latin-1 -*-\nx = 'é'\n".encode("latin-1"))
    latin_module = astroid.MANAGER.ast_from_file(str(path), "latin")
    assert source_segment(latin_module.body[0].value) == "'é'"


@pytest.mark.parametrize(
    "raw",
    [
        b"x = 1\r\ny = 2\r\n",
        b"\xef\xbb\xbfx = 1\n",
        "# -*- coding: latin-1 -*-\nx = 'é'\n".encode("latin-1"),
    ],
    ids=["crlf", "bom", "latin-1"],
)
def test_read_and_write_source_round_trip(tmp_path: Path, raw: bytes) -> None:
    path = str(tmp_path / "file.py")
    Path(path).write_bytes(raw)
    source, encoding = read_source(path)
    write_source(path, source, encoding)
    assert Path(path).read_bytes() == raw


def test_crlf_line_endings_are_kept() -> None:
    result = apply_fixes("x = 1\r\ny = 2\r\n", [_fix(Edit(2, 4, 2, 5, "3"))], SAFE)
    assert result.source == "x = 1\r\ny = 3\r\n"


class TestAddMessageWithFix:
    @staticmethod
    def _linter_with_module(source: str) -> tuple[PyLinter, nodes.Module]:
        linter = PyLinter()
        linter.load_default_plugins()
        linter.set_reporter(CollectingReporter())
        module = astroid.parse(source, module_name="fruits", path="fruits.py")
        linter.set_current_module("fruits", "fruits.py")
        linter.file_state._module = module
        return linter, module

    def test_fix_of_a_non_fixable_message_raises(self) -> None:
        linter, module = self._linter_with_module("x = 1\n")
        node = module.body[0]
        with pytest.raises(InvalidMessageError, match="has no fixer"):
            linter.add_message(
                "pointless-statement",
                node=node,
                fix=_fix(Edit(1, 0, 1, 1, "y")),
            )

    def test_lazy_fix_is_resolved_and_attached(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        linter, module = self._linter_with_module("x = 1\n")
        node = module.body[0]
        definition = linter.msgs_store.get_message_definitions("pointless-statement")
        monkeypatch.setattr(definition[0], "fixable", True)
        fix = _fix(Edit.replace(node, "y = 1"))
        linter.add_message("pointless-statement", node=node, fix=lambda: fix)
        assert linter.reporter.messages[0].fix == fix
        assert linter._available_fixes[Applicability.SAFE] == 1

    def test_lazy_fix_is_not_built_for_a_disabled_message(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        linter, module = self._linter_with_module("x = 1\n")
        definition = linter.msgs_store.get_message_definitions("pointless-statement")
        monkeypatch.setattr(definition[0], "fixable", True)
        linter.disable("pointless-statement")

        def build_fix() -> Fix:
            raise AssertionError("The fix of a disabled message was built")

        linter.add_message("pointless-statement", node=module.body[0], fix=build_fix)
        assert not linter.reporter.messages

    def test_fix_editing_another_file_is_dropped(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        linter, module = self._linter_with_module("x = 1\n")
        definition = linter.msgs_store.get_message_definitions("pointless-statement")
        monkeypatch.setattr(definition[0], "fixable", True)
        other_module = astroid.parse("y = 2\n", module_name="other", path="other.py")
        fix = _fix(Edit.replace(other_module.body[0], "z = 2"))
        linter.add_message("pointless-statement", node=module.body[0], fix=fix)
        assert linter.reporter.messages[0].fix is None


def test_source_tokens_use_edit_positions() -> None:
    module = astroid.parse('x = "é"; y = any([1 for a in b],  # comment\n)\n')
    tokens = source_tokens(module.body[1].value)
    assert tokens is not None
    strings = [token.string for token in tokens if token.string.strip()]
    assert strings == [
        "any",
        "(",
        "[",
        "1",
        "for",
        "a",
        "in",
        "b",
        "]",
        ",",
        "# comment",
        ")",
    ]
    comma = next(token for token in tokens if token.string == ",")
    # 'é' is two bytes long in UTF-8
    assert (comma.start, comma.end) == ((1, 32), (1, 33))
    assert source_tokens(nodes.Const(1)) is None


class _FruitChecker(BaseChecker):
    name = "fruit"
    msgs = {
        "W9801": ("Rotten %s apple", "rotten-apple", "Used to test fixers."),
        "W9802": ("Green banana", "green-banana", "Not fixable."),
    }

    def __init__(self, linter: PyLinter) -> None:
        super().__init__(linter)
        self.fixer_calls: list[dict[str, Any]] = []

    def fix_rotten_apple(self, node: nodes.NodeNG, **kwargs: Any) -> Fix | None:
        self.fixer_calls.append(kwargs)
        return Fix.create("Replace the apple", Edit.replace(node, "fresh_apple"))


class TestFixerDiscovery:
    @staticmethod
    def _linter_and_checker() -> tuple[PyLinter, _FruitChecker, nodes.Module]:
        linter = PyLinter()
        linter.set_reporter(CollectingReporter())
        checker = _FruitChecker(linter)
        linter.register_checker(checker)
        module = astroid.parse("apple\n", module_name="fruits", path="fruits.py")
        linter.set_current_module("fruits", "fruits.py")
        linter.file_state._module = module
        return linter, checker, module

    def test_a_message_with_a_fixer_is_fixable(self) -> None:
        linter, _, _ = self._linter_and_checker()
        store = linter.msgs_store
        assert store.get_message_definitions("rotten-apple")[0].fixable
        assert not store.get_message_definitions("green-banana")[0].fixable
        assert (
            "can be fixed automatically"
            in store.get_message_definitions("W9801")[0].format_help()
        )

    def test_the_fixer_gets_the_node_and_the_arguments(self) -> None:
        linter, checker, module = self._linter_and_checker()
        node = module.body[0].value
        checker.add_message("rotten-apple", node=node, args=("red",))
        checker.add_message("W9801", node=node, args=("green",))
        checker.add_message("green-banana", node=node)
        fixes = [message.fix for message in linter.reporter.messages]
        expected = Fix("Replace the apple", (Edit.replace(node, "fresh_apple"),))  # type: ignore[arg-type]
        assert fixes == [expected, expected, None]
        assert checker.fixer_calls[0] == {
            "line": None,
            "args": ("red",),
            "confidence": UNDEFINED,
            "col_offset": None,
            "end_lineno": None,
            "end_col_offset": None,
        }

    def test_the_fixer_is_not_called_for_a_disabled_message(self) -> None:
        linter, checker, module = self._linter_and_checker()
        linter.disable("rotten-apple")
        checker.add_message("rotten-apple", node=module.body[0].value)
        assert not linter.reporter.messages
        assert not checker.fixer_calls

    def test_a_fixer_without_message_raises(self) -> None:
        class TypoChecker(_FruitChecker):
            def fix_roten_apple(self, _node: nodes.NodeNG, **_: Any) -> Fix | None:
                return None

        linter = PyLinter()
        with pytest.raises(InvalidMessageError, match="'fix_roten_apple' of the"):
            linter.register_checker(TypoChecker(linter))

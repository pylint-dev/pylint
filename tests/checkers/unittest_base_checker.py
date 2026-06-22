# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the BaseChecker class."""

import astroid
import pytest

from pylint.checkers import BaseChecker
from pylint.checkers.imports import ImportsChecker
from pylint.checkers.typecheck import TypeChecker
from pylint.exceptions import InvalidMessageError
from pylint.extensions.broad_try_clause import BroadTryClauseChecker
from pylint.extensions.while_used import WhileChecker
from pylint.interfaces import HIGH
from pylint.lint.pylinter import PyLinter
from pylint.testutils import UnittestLinter


class OtherBasicChecker(BaseChecker):
    def __init__(self) -> None:
        super().__init__(PyLinter())

    name = "basic"
    msgs = {
        "W0001": (
            "Basic checker has an example.",
            "basic-checker-example",
            "Used nowhere and serves no purpose.",
        )
    }


class MissingFieldsChecker(BaseChecker):
    name = "basic"
    msgs = {"W0001": ("msg-name",)}  # type: ignore[dict-item]


class LessBasicChecker(OtherBasicChecker):
    options = (
        (
            "example-args",
            {
                "default": 42,
                "type": "int",
                "metavar": "<int>",
                "help": "Example of integer argument for the checker.",
            },
        ),
    )


class DifferentBasicChecker(BaseChecker):
    def __init__(self) -> None:
        super().__init__(PyLinter())

    name = "a-different-checker"
    msgs = {
        "W0002": (
            "Blah blah example.",
            "blah-blah-example",
            "I only exist to be different to OtherBasicChecker :(",
        )
    }


class MessageWithOptionsChecker(BaseChecker):
    name = "message-with-options-checker"
    msgs = {
        "W0003": (
            "Just a message with pre-defined options %s()",
            "message-with-options",
            "Message with options dict to test consistent hashing.",
            {"old_names": [("W1003", "old-message-with-options")], "shared": True},
        ),
    }


def test_base_checker_doc() -> None:
    basic = OtherBasicChecker()
    expected_beginning = """\
Basic checker
~~~~~~~~~~~~~

Verbatim name of the checker is ``basic``.

"""
    expected_middle = """\
Basic checker Options
^^^^^^^^^^^^^^^^^^^^^
:example-args:
  Example of integer argument for the checker.

  Default: ``42``

"""
    expected_end = """\
Basic checker Messages
^^^^^^^^^^^^^^^^^^^^^^
:basic-checker-example (W0001): *Basic checker has an example.*
  Used nowhere and serves no purpose.


"""
    assert str(basic) == expected_beginning + expected_end
    assert repr(basic) == "Checker 'basic' (responsible for 'W0001')"
    less_basic = LessBasicChecker()

    assert str(less_basic) == expected_beginning + expected_middle + expected_end
    assert repr(less_basic) == repr(basic)


def test_base_checker_ordering() -> None:
    """Test ordering of checkers based on their __gt__ method."""
    linter = PyLinter()
    imports_builtin = ImportsChecker(linter)
    typecheck_builtin = TypeChecker(linter)
    basic_1_ext = OtherBasicChecker()
    basic_2_ext = LessBasicChecker()
    basic_3_ext = DifferentBasicChecker()
    while_used_ext = WhileChecker(linter)
    broad_try_clause_ext = BroadTryClauseChecker(linter)

    list_of_checkers = [
        1,
        basic_1_ext,
        basic_2_ext,
        basic_3_ext,
        typecheck_builtin,
        broad_try_clause_ext,
        imports_builtin,
        while_used_ext,
        linter,
    ]
    assert sorted(list_of_checkers) == [  # type: ignore[type-var]
        linter,
        imports_builtin,
        typecheck_builtin,
        basic_3_ext,
        basic_1_ext,
        basic_2_ext,
        broad_try_clause_ext,
        while_used_ext,
        1,
    ]
    # main checker is always smaller
    assert linter < basic_1_ext
    assert linter < while_used_ext
    assert linter < imports_builtin
    assert basic_2_ext > linter
    assert while_used_ext > linter
    assert imports_builtin > linter
    # builtin are smaller than extension (even when not alphabetically)
    assert imports_builtin < while_used_ext
    assert imports_builtin < broad_try_clause_ext
    assert while_used_ext > imports_builtin
    assert broad_try_clause_ext > imports_builtin
    # alphabetical order for builtin
    assert imports_builtin < typecheck_builtin
    assert typecheck_builtin > imports_builtin
    # alphabetical order for extension
    assert typecheck_builtin < while_used_ext
    assert while_used_ext > typecheck_builtin
    assert basic_1_ext > basic_3_ext
    assert basic_2_ext > basic_3_ext
    assert basic_1_ext == basic_2_ext


def test_base_checker_invalid_message() -> None:
    linter = PyLinter()
    with pytest.raises(InvalidMessageError):
        linter.register_checker(MissingFieldsChecker(linter))


def test_base_checker_consistent_hash() -> None:
    linter = PyLinter()
    checker = MessageWithOptionsChecker(linter)
    some_set = {checker}

    original_hash = hash(checker)
    assert checker in some_set

    for msgid, msg in checker.msgs.items():
        checker.create_message_definition_from_tuple(msgid, msg)

    assert hash(checker) == original_hash
    assert checker in some_set


class _DelegationChecker(BaseChecker):
    """Minimal checker used to exercise ``add_message_at_*`` delegation."""

    name = "delegation-checker"
    msgs = {
        "W9999": (
            "Delegation test %s",
            "delegation-test",
            "Used in tests to exercise add_message_at_* delegation.",
        ),
    }


def test_base_checker_add_message_at_node_delegates() -> None:
    """``BaseChecker.add_message_at_node`` forwards to the linter and captures."""
    linter = UnittestLinter()
    checker = _DelegationChecker(linter)
    linter.register_checker(checker)

    module_node = astroid.parse("def foo(): pass", module_name="m")
    node = module_node.body[0]
    checker.add_message_at_node("W9999", node, args=("hello",), confidence=HIGH)

    messages = linter.release_messages()
    assert len(messages) == 1
    assert messages[0].msg_id == "W9999"
    assert messages[0].args == ("hello",)
    assert messages[0].confidence == HIGH


def test_base_checker_add_message_at_location_delegates() -> None:
    """``BaseChecker.add_message_at_location`` forwards to the linter and captures."""
    linter = UnittestLinter()
    checker = _DelegationChecker(linter)
    linter.register_checker(checker)

    checker.add_message_at_location(
        "W9999",
        module="other_module",
        filepath="other.py",
        line=42,
        col_offset=3,
        args=("world",),
        confidence=HIGH,
    )

    messages = linter.release_messages()
    assert len(messages) == 1
    assert messages[0].msg_id == "W9999"
    assert messages[0].line == 42
    assert messages[0].col_offset == 3
    assert messages[0].args == ("world",)

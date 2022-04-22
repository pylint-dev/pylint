# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import warnings

import astroid

from pylint.checkers.utils import only_required_for_messages
from pylint.utils import ASTWalker


class TestASTWalker:
    class MockLinter:
        def __init__(self, msgs: dict[str, bool]) -> None:
            self._msgs = msgs

        def is_message_enabled(self, msgid: str) -> bool:
            return self._msgs.get(msgid, True)

    class Checker:
        def __init__(self) -> None:
            self.called: set[str] = set()

        @only_required_for_messages("first-message")
        def visit_module(self, module):  # pylint: disable=unused-argument
            self.called.add("module")

        @only_required_for_messages("second-message")
        def visit_call(self, module):
            raise NotImplementedError

        @only_required_for_messages("second-message", "third-message")
        def visit_assignname(self, module):  # pylint: disable=unused-argument
            self.called.add("assignname")

        @only_required_for_messages("second-message")
        def leave_assignname(self, module):
            raise NotImplementedError

    def test_only_required_for_messages(self) -> None:
        linter = self.MockLinter(
            {"first-message": True, "second-message": False, "third-message": True}
        )
        walker = ASTWalker(linter)  # type: ignore[arg-type]
        checker = self.Checker()
        walker.add_checker(checker)  # type: ignore[arg-type]
        walker.walk(astroid.parse("x = func()"))
        assert {"module", "assignname"} == checker.called

    def test_deprecated_methods(self) -> None:
        class Checker:
            def __init__(self) -> None:
                self.called = False

            @only_required_for_messages("first-message")
            def visit_assname(self, node):  # pylint: disable=unused-argument
                self.called = True

        linter = self.MockLinter({"first-message": True})
        walker = ASTWalker(linter)  # type: ignore[arg-type]
        checker = Checker()
        walker.add_checker(checker)  # type: ignore[arg-type]
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            walker.walk(astroid.parse("x = 1"))

            assert not checker.called

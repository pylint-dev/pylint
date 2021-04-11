# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE

import warnings

import astroid

from pylint.checkers.utils import check_messages
from pylint.utils import ASTWalker


class TestASTWalker:
    class MockLinter:
        def __init__(self, msgs):
            self._msgs = msgs

        def is_message_enabled(self, msgid):
            return self._msgs.get(msgid, True)

    class Checker:
        def __init__(self):
            self.called = set()

        @check_messages("first-message")
        def visit_module(self, module):  # pylint: disable=unused-argument
            self.called.add("module")

        @check_messages("second-message")
        def visit_call(self, module):
            raise NotImplementedError

        @check_messages("second-message", "third-message")
        def visit_assignname(self, module):  # pylint: disable=unused-argument
            self.called.add("assignname")

        @check_messages("second-message")
        def leave_assignname(self, module):
            raise NotImplementedError

    def test_check_messages(self):
        linter = self.MockLinter(
            {"first-message": True, "second-message": False, "third-message": True}
        )
        walker = ASTWalker(linter)
        checker = self.Checker()
        walker.add_checker(checker)
        walker.walk(astroid.parse("x = func()"))
        assert {"module", "assignname"} == checker.called

    def test_deprecated_methods(self):
        class Checker:
            def __init__(self):
                self.called = False

            @check_messages("first-message")
            def visit_assname(self, node):  # pylint: disable=unused-argument
                self.called = True

        linter = self.MockLinter({"first-message": True})
        walker = ASTWalker(linter)
        checker = Checker()
        walker.add_checker(checker)
        with warnings.catch_warnings(record=True):
            warnings.simplefilter("always")
            walker.walk(astroid.parse("x = 1"))

            assert not checker.called

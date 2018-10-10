# Copyright (c) 2015-2018 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import astroid

from pylint.checkers import strings
from pylint.testutils import CheckerTestCase, Message


TEST_TOKENS = (
    '"X"',
    "'X'",
    "'''X'''",
    '"""X"""',
    'r"X"',
    "R'X'",
    'u"X"',
    "F'X'",
    'f"X"',
    "F'X'",
    'fr"X"',
    'Fr"X"',
    'fR"X"',
    'FR"X"',
    'rf"X"',
    'rF"X"',
    'Rf"X"',
    'RF"X"',
)


class TestStringChecker(CheckerTestCase):
    CHECKER_CLASS = strings.StringFormatChecker

    def test_format_bytes(self):
        code = "b'test'.format(1, 2)"
        node = astroid.extract_node(code)
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_format_types(self):
        for code in ("'%s' % 1", "'%d' % 1", "'%f' % 1"):
            with self.assertNoMessages():
                node = astroid.extract_node(code)
            self.checker.visit_binop(node)

        for code in (
            "'%s' % 1",
            "'%(key)s' % {'key' : 1}",
            "'%d' % 1",
            "'%(key)d' % {'key' : 1}",
            "'%f' % 1",
            "'%(key)f' % {'key' : 1}",
            "'%d' % 1.1",
            "'%(key)d' % {'key' : 1.1}",
            "'%s' % []",
            "'%(key)s' % {'key' : []}",
            "'%s' % None",
            "'%(key)s' % {'key' : None}",
        ):
            with self.assertNoMessages():
                node = astroid.extract_node(code)
                self.checker.visit_binop(node)

        for code, arg_type, format_type in [
            ("'%d' % '1'", "builtins.str", "d"),
            ("'%(key)d' % {'key' : '1'}", "builtins.str", "d"),
            ("'%x' % 1.1", "builtins.float", "x"),
            ("'%(key)x' % {'key' : 1.1}", "builtins.float", "x"),
            ("'%d' % []", "builtins.list", "d"),
            ("'%(key)d' % {'key' : []}", "builtins.list", "d"),
        ]:
            node = astroid.extract_node(code)
            with self.assertAddsMessages(
                Message(
                    "bad-string-format-type", node=node, args=(arg_type, format_type)
                )
            ):
                self.checker.visit_binop(node)

    def test_str_eval(self):
        for token in TEST_TOKENS:
            assert strings.str_eval(token) == "X"

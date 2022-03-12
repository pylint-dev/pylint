# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/graphs/contributors


from pylint.checkers import strings

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


def test_str_eval() -> None:
    for token in TEST_TOKENS:
        assert strings.str_eval(token) == "X"

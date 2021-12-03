# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2016 Derek Gustafson <degustaf@gmail.com>
# Copyright (c) 2018 Lucas Cimon <lucas.cimon@gmail.com>
# Copyright (c) 2018 Yury Gribov <tetra2005@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Ashley Whetter <ashley@awhetter.co.uk>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE


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

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the BaseChecker class."""


from pylint.checkers import BaseChecker
from pylint.checkers.imports import ImportsChecker
from pylint.checkers.typecheck import TypeChecker
from pylint.extensions.while_used import WhileChecker
from pylint.lint.pylinter import PyLinter


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
    fake_checker_1 = OtherBasicChecker()
    fake_checker_2 = LessBasicChecker()
    fake_checker_3 = DifferentBasicChecker()
    import_checker = ImportsChecker(linter)
    while_checker = WhileChecker(linter)
    type_checker = TypeChecker(linter)

    list_of_checkers = [
        1,
        fake_checker_1,
        fake_checker_2,
        fake_checker_3,
        type_checker,
        import_checker,
        while_checker,
        linter,
    ]
    assert sorted(list_of_checkers) == [  # type: ignore[type-var]
        linter,
        import_checker,
        type_checker,
        fake_checker_3,
        fake_checker_1,
        fake_checker_2,
        while_checker,
        1,
    ]
    assert fake_checker_1 > fake_checker_3
    assert fake_checker_2 > fake_checker_3
    assert fake_checker_1 == fake_checker_2

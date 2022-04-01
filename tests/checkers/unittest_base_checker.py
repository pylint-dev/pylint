# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Unittest for the BaseChecker class."""


from pylint.checkers import BaseChecker


class OtherBasicChecker(BaseChecker):
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
    name = "different"
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
    fake_checker_1 = OtherBasicChecker()
    fake_checker_2 = LessBasicChecker()
    fake_checker_3 = DifferentBasicChecker()
    assert fake_checker_1 < fake_checker_3
    assert fake_checker_2 < fake_checker_3
    assert fake_checker_1 == fake_checker_2

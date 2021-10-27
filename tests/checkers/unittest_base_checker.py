# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Unittest for the BaseChecker class."""

import unittest

from pylint.checkers import BaseChecker


class TestBaseChecker(unittest.TestCase):
    def test_doc(self) -> None:
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
        self.assertEqual(str(basic), expected_beginning + expected_end)
        self.assertEqual(repr(basic), "Checker 'basic' (responsible for 'W0001')")
        less_basic = LessBasicChecker()

        self.assertEqual(
            str(less_basic), expected_beginning + expected_middle + expected_end
        )
        self.assertEqual(repr(less_basic), repr(basic))

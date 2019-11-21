import sys
from os.path import abspath, dirname, join

from pylint.lint import Run

HERE = abspath(dirname(__file__))


def test_fail_under_plus():
    try:
        run = Run(["--fail-under", "-1", join(HERE, "input", "fail_under_plus6.py")])
    except SystemExit as ex:
        assert ex.code == 0


def test_fail_under_minus():
    try:
        run = Run(["--fail-under", "-1", join(HERE, "input", "fail_under_minus6.py")])
    except SystemExit as ex:
        assert ex.code != 0

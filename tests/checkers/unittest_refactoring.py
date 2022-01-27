# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
import signal
from contextlib import contextmanager

import pytest

from pylint.lint import Run
from pylint.reporters.text import TextReporter

PARENT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
REGR_DATA = os.path.join(PARENT_DIR, "regrtest_data")


@contextmanager
def timeout(timeout_s: float):
    def _handle(_signum, _frame):
        pytest.fail("Test took too long")

    signal.signal(signal.SIGALRM, _handle)
    signal.setitimer(signal.ITIMER_REAL, timeout_s)
    yield
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, signal.SIG_DFL)


@pytest.mark.skipif(not hasattr(signal, "setitimer"), reason="Assumes POSIX signals")
def test_process_tokens() -> None:
    with timeout(8.0):
        with pytest.raises(SystemExit) as cm:
            Run([os.path.join(REGR_DATA, "very_long_line.py")], reporter=TextReporter())
        assert cm.value.code == 0

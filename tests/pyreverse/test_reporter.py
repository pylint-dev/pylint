# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import sys

from pylint.reporters import BaseReporter


def test_deprecation_set_output(recwarn):
    """TODO remove in 3.0"""  # pylint: disable=fixme
    reporter = BaseReporter()
    reporter.set_output(sys.stdout)
    warning = recwarn.pop()
    assert "set_output' will be removed in 3.0" in str(warning)
    assert reporter.out == sys.stdout

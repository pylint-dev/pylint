# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

__all__ = [
    "FunctionalTestFile",
    "NoFileError",
    "parse_python_version",
]

import warnings

from pylint.testutils.functional import (
    FunctionalTestFile,
    NoFileError,
    parse_python_version,
)

warnings.warn(
    "'pylint.testutils.functional_test_file' will be accessible by"
    " the 'pylint.testutils.functional' API in pylint 3.0",
    DeprecationWarning,
)

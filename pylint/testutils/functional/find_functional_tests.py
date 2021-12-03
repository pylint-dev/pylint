# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
from pathlib import Path
from typing import List, Union

from pylint.testutils.functional.test_file import FunctionalTestFile

# 'Wet finger' number of files that are reasonable to display by an IDE
# 'Wet finger' as in 'in my settings there are precisely this many'.
REASONABLY_DISPLAYABLE_VERTICALLY = 48


def get_functional_test_files_from_directory(
    input_dir: Union[Path, str]
) -> List[FunctionalTestFile]:
    """Get all functional tests in the input_dir."""
    suite = []
    for dirpath, _, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue

        assert (
            len(filenames) <= REASONABLY_DISPLAYABLE_VERTICALLY
        ), f"{dirpath} contains too many functional tests files."

        for filename in filenames:
            if filename != "__init__.py" and filename.endswith(".py"):
                suite.append(FunctionalTestFile(dirpath, filename))
    return suite

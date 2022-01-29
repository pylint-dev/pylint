# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

import os
from pathlib import Path
from typing import List, Union

from pylint.testutils.functional.test_file import FunctionalTestFile

# 'Wet finger' number of files that are reasonable to display by an IDE
# 'Wet finger' as in 'in my settings there are precisely this many'.
REASONABLY_DISPLAYABLE_VERTICALLY = 48
SHOULD_BE_IN_THE_SAME_DIRECTORY = 5


def get_functional_test_files_from_directory(
    input_dir: Union[Path, str],
    reasonably_displayable_vertically: int = REASONABLY_DISPLAYABLE_VERTICALLY,
) -> List[FunctionalTestFile]:
    """Get all functional tests in the input_dir."""
    suite = []
    for dirpath, dirnames, filenames in os.walk(input_dir):
        if dirpath.endswith("__pycache__"):
            continue
        check_functional_tests_structure(
            dirpath,
            dirnames,
            filenames,
            str(input_dir),
            reasonably_displayable_vertically,
        )
        for filename in filenames:
            if filename != "__init__.py" and filename.endswith(".py"):
                suite.append(FunctionalTestFile(dirpath, filename))
    return suite


def check_functional_tests_structure(
    dirpath: str,
    dirnames: List[str],
    filenames: List[str],
    input_dir: str,
    reasonably_displayable_vertically: int,
) -> None:
    assert (
        len(filenames) <= reasonably_displayable_vertically
    ), f"{dirpath} contains too many functional tests files."
    if dirpath == input_dir:
        return
    last_dir_name = dirpath.split("/")[-1].lstrip()
    # print(f"{dirpath=} {dirnames=} {filenames=} {last_dir_name=}")
    for filename in filenames:
        if filename.startswith("__"):
            return
        f"'{filename}' incorrectly located in '{dirpath}' (should start with '{last_dir_name}')"
        # assert filename.startswith(last_dir_name), msg

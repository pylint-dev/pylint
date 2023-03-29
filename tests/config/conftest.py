# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

import pytest

HERE = Path(__file__).parent


@pytest.fixture()
def file_to_lint_path() -> str:
    return str(HERE / "file_to_lint.py")

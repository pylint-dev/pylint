from pathlib import Path

import pytest

HERE = Path(__file__).parent


@pytest.fixture()
def file_to_lint_path() -> str:
    return str(HERE / "file_to_lint.py")

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

import tempfile
from pathlib import Path

from pylint.lint import Run


def test_fall_back_on_base_config() -> None:
    """Test that we correctly fall back on the base config."""
    # A file under the current dir should fall back to the highest level
    # For pylint this is ./pylintrc
    runner = Run([__name__], exit=False)
    assert id(runner.linter.config) == id(runner.linter._base_config)

    # When the file is a directory that does not have any of its parents in
    # linter._directory_namespaces it should default to the base config
    with tempfile.TemporaryDirectory() as tmpdir:
        with open(Path(tmpdir) / "test.py", "w", encoding="utf-8") as f:
            f.write("1")
        Run([str(Path(tmpdir) / "test.py")], exit=False)
        assert id(runner.linter.config) == id(runner.linter._base_config)

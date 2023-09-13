# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from pathlib import Path

from pylint.testutils._run import _Run as Run


def test_fall_back_on_base_config(tmp_path: Path) -> None:
    """Test that we correctly fall back on the base config."""
    # A file under the current dir should fall back to the highest level
    # For pylint this is ./pylintrc
    test_file = tmp_path / "test.py"
    runner = Run([__name__], exit=False)
    assert id(runner.linter.config) == id(runner.linter._base_config)

    # When the file is a directory that does not have any of its parents in
    # linter._directory_namespaces it should default to the base config
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("1")
    Run([str(test_file)], exit=False)
    assert id(runner.linter.config) == id(runner.linter._base_config)

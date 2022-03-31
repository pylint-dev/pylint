# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt
from pathlib import Path

import pytest

from pylint.config.find_default_config_files import _cfg_has_config, _toml_has_config


@pytest.mark.parametrize(
    "content,expected",
    [
        ["", False],
        ["(not toml valid)", False],
        [
            """
[build-system]
requires = ["setuptools ~= 58.0", "cython ~= 0.29.0"]
""",
            False,
        ],
        [
            """
[tool.pylint]
missing-member-hint = true
""",
            True,
        ],
    ],
)
def test_toml_has_config(content: str, expected: bool, tmp_path: Path) -> None:
    """Test that a toml file has a pylint config."""
    fake_toml = tmp_path / "fake.toml"
    with open(fake_toml, "w", encoding="utf8") as f:
        f.write(content)
    assert _toml_has_config(fake_toml) == expected


@pytest.mark.parametrize(
    "content,expected",
    [
        ["", False],
        ["(not valid .cfg)", False],
        [
            """
[metadata]
name = pylint
""",
            False,
        ],
        [
            """
[metadata]
name = pylint

[pylint.messages control]
disable = logging-not-lazy,logging-format-interpolation
""",
            True,
        ],
    ],
)
def test_cfg_has_config(content: str, expected: str, tmp_path: Path) -> None:
    """Test that a cfg file has a pylint config."""
    fake_cfg = tmp_path / "fake.cfg"
    with open(fake_cfg, "w", encoding="utf8") as f:
        f.write(content)
    assert _cfg_has_config(fake_cfg) == expected

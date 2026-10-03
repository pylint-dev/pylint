# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/4899

``pydantic.dataclasses.dataclass`` with ``items: list = field(default_factory=lambda: [])``
used to mis-infer ``items`` as the ``dataclasses.Field`` descriptor itself,
emitting false ``no-member`` on ``.append`` and ``not-an-iterable`` on
iteration. Confirm the FP is gone when pydantic is available.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("pydantic", reason="pydantic is required to reproduce #4899")


def test_pydantic_field_default_factory_no_false_no_member(tmp_path: Path) -> None:
    """A ``field(default_factory=lambda: [])`` attribute keeps its list type."""
    (tmp_path / "cases.py").write_text(
        '"""Module."""\n'
        "from dataclasses import field\n"
        "from typing import List\n"
        "from pydantic.dataclasses import dataclass\n"
        "\n"
        "\n"
        "@dataclass\n"
        "class Item:\n"
        '    """Item."""\n'
        '    description: str = ""\n'
        "\n"
        "\n"
        "@dataclass\n"
        "class Case:\n"
        '    """Case."""\n'
        "    name: str\n"
        "    irr: float = 0\n"
        "    items: List[Item] = field(default_factory=lambda: [])\n"
        "\n"
        "    def add_item(self, item: Item) -> None:\n"
        '        """Append."""\n'
        "        self.items.append(item)\n"
        "\n"
        "    def find_item(self, description: str):\n"
        '        """Find."""\n'
        "        return next(\n"
        "            (item for item in self.items if item.description == description),\n"
        "            None,\n"
        "        )\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--disable=all",
            "--enable=no-member,not-an-iterable",
            "cases.py",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "no-member" not in output, f"#4899 regression (no-member): {output!r}"
    assert (
        "not-an-iterable" not in output
    ), f"#4899 regression (not-an-iterable): {output!r}"

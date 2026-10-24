# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/4917

A variable bound by ``with CtxMgr() as x: x = OtherClass(...)`` was once
treated as an instance of the context-manager class, producing a false
``no-member`` on ``x.method_of_other_class()``. Confirm pylint now infers
the rebinding correctly.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_with_block_rebinding_no_false_no_member(tmp_path: Path) -> None:
    """Rebinding inside a ``with`` block must not trigger no-member on the new type."""
    (tmp_path / "animal_api.py").write_text(
        '"""Module."""\n'
        "\n"
        "\n"
        "class Animal:\n"
        '    """Animal."""\n'
        '    def __init__(self, name=""):\n'
        "        self.name = name\n"
        "\n"
        "    def add_animal_to_db(self, _uow):\n"
        '        """Persist."""\n'
        "        return self\n"
        "\n"
        "    def as_dict(self):\n"
        '        """Serialize."""\n'
        '        return {"name": self.name}\n'
        "\n"
        "\n"
        "class SQLUnitOfWork:\n"
        '    """SQLUnitOfWork."""\n'
        "    def __init__(self, config):\n"
        "        self.config = config\n"
        "\n"
        "    def __enter__(self):\n"
        "        return self\n"
        "\n"
        "    def __exit__(self, *args):\n"
        "        return None\n"
        "\n"
        "\n"
        "def handler(data, config, body):\n"
        '    """Handler."""\n'
        "    with SQLUnitOfWork(config) as uow:\n"
        "        animal = Animal(**data).add_animal_to_db(uow)\n"
        "        if not animal:\n"
        '            return {"status": "Incorrect values", "values": body}, 405\n'
        "        return animal.as_dict(), 201\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--disable=all",
            "--enable=no-member",
            "animal_api.py",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "no-member" not in output, f"#4917 regression: {output!r}"

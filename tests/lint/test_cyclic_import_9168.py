# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/9168

The reporter says `cyclic-import` is detected on Linux but not on macOS
for the same project layout. This test exercises the layout on whatever
platform the CI runs on; if the bug is real, the assertion will fail on
macOS only.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_cyclic_import_detected_in_package(tmp_path: Path) -> None:
    """Reproduce the directory layout from #9168 and assert cyclic-import fires."""
    pkg = tmp_path / "module1"
    pkg.mkdir()
    (pkg / "__init__.py").write_text(
        "from module1.base import Base\n" "from module1.derived import Derived\n"
    )
    (pkg / "base.py").write_text(
        "class Base:\n" "    def __init__(self):\n" "        print('hello from base')\n"
    )
    (pkg / "derived.py").write_text(
        "from module1 import Base\n"
        "\n"
        "class Derived(Base):\n"
        "    def __init__(self):\n"
        "        super().__init__()\n"
        "        print('hello from derived')\n"
    )
    (tmp_path / "main.py").write_text(
        "from module1 import Derived\n"
        "\n"
        "if __name__ == '__main__':\n"
        "    Derived()\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--recursive=y",
            "--disable=W,C0114,C0115,C0116,R0903",
            "-s=n",
            ".",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "cyclic-import" in output, (
        f"Expected cyclic-import to be reported on {sys.platform}, " f"got: {output!r}"
    )

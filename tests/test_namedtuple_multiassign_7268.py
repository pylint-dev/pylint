# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/7268

The reporter had pylint crash on a ``NamedTuple`` subclass that assigned
its members on one line with tuple-unpacking. Confirm the astroid
``infer_typing_namedtuple_class`` brain no longer crashes on this shape.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_namedtuple_multi_assignment_does_not_crash(tmp_path: Path) -> None:
    """A NamedTuple with tuple-unpacked attribute assignment should not crash."""
    (tmp_path / "color.py").write_text(
        "from typing import NamedTuple\n"
        "\n"
        "class Color(NamedTuple):\n"
        "    RED, CYAN, BLUE, BLACK, GREEN, WHITE = 31, 36, 34, 30, 32, 37\n"
    )

    process = subprocess.run(
        [sys.executable, "-m", "pylint", "color.py"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "Traceback" not in output, f"pylint crashed on Py {sys.version}: {output!r}"
    assert "astroid-error" not in output, f"astroid error: {output!r}"
    assert "F0002" not in output, f"fatal error: {output!r}"

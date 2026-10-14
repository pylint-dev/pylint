# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/9983

When an f-string keyword name is uninferable, pylint used to emit
``unexpected-keyword-arg`` with ``'Uninferable_factory'`` in the message
text — a synthetic name nobody would ever write. Confirm the FP is gone.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_uninferable_kwargs_no_false_positive(tmp_path: Path) -> None:
    """A ``**{f"{name}_factory": ...}`` call must not raise unexpected-keyword-arg."""
    (tmp_path / "module.py").write_text(
        '"""Module."""\n'
        "\n"
        "\n"
        "class Registry:\n"
        '    """Registry."""\n'
        "    def __init__(self, **kwargs):\n"
        "        self.kwargs = kwargs\n"
        "\n"
        "\n"
        "def make(name, factory):\n"
        '    """Make."""\n'
        '    return Registry(**{f"{name}_factory": factory})\n'
    )

    process = subprocess.run(
        [sys.executable, "-m", "pylint", "module.py"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert (
        "unexpected-keyword-arg" not in output
    ), f"#9983 regression: got unexpected-keyword-arg FP: {output!r}"
    assert (
        "Uninferable_factory" not in output
    ), f"#9983 regression: synthetic Uninferable name leaked: {output!r}"

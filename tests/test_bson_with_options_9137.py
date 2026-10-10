# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/9137

``LEGACY_JSON_OPTIONS.with_options(tz_aware=True, tzinfo=...)`` used to
crash pylint with ``'UninferableBase' object is not iterable``. Confirm
inference no longer blows up when bson is available.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip(
    "bson.json_util", reason="pymongo (bson) is required to reproduce #9137"
)
pytest.importorskip("pytz", reason="pytz is required to reproduce #9137")


def test_bson_with_options_does_not_crash(tmp_path: Path) -> None:
    """``LEGACY_JSON_OPTIONS.with_options(...)`` must not crash inference."""
    (tmp_path / "json_util.py").write_text(
        '"""JSON util."""\n'
        "import pytz\n"
        "from bson.json_util import LEGACY_JSON_OPTIONS\n"
        "\n"
        "CUSTOM_JSON_OPTIONS = LEGACY_JSON_OPTIONS.with_options(\n"
        "    tz_aware=True, tzinfo=pytz.UTC\n"
        ")\n"
    )

    process = subprocess.run(
        [sys.executable, "-m", "pylint", "json_util.py"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "UninferableBase" not in output, f"#9137 regression: {output!r}"
    assert "Traceback" not in output, f"#9137 regression (crash): {output!r}"
    assert (
        "astroid-error" not in output
    ), f"#9137 regression (astroid-error): {output!r}"

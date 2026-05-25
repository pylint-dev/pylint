# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/7122

``src_records.binaries`` and ``fetcher.items`` from ``apt_pkg`` get a
false ``not-an-iterable`` (E1133) even though the stubs declare them as
``List[str]``. This test asserts the FP is **present** today: when CI is
red, the bug is still real. Linux-only since apt_pkg is Debian/Ubuntu.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("apt", reason="python3-apt is required to reproduce #7122")
pytest.importorskip("apt_pkg", reason="python3-apt is required to reproduce #7122")


def test_apt_pkg_iterable_attributes_trigger_not_an_iterable(tmp_path: Path) -> None:
    """``apt_pkg`` attributes typed as List in stubs still trip not-an-iterable."""
    (tmp_path / "example.py").write_text(
        "#!/usr/bin/python3\n"
        "# pylint: disable=missing-docstring\n"
        "\n"
        "import os\n"
        "import apt\n"
        "\n"
        "src_records = apt.apt_pkg.SourceRecords()\n"
        'src_records.lookup("bash")\n'
        'pkgs = [p for p in src_records.binaries if not p.endswith("-doc")]\n'
        "print(pkgs)\n"
        "\n"
        "fetcher = apt.apt_pkg.Acquire(apt.progress.text.AcquireProgress())\n"
        "cache = apt.Cache(rootdir=os.getcwd())\n"
        "cache.fetch_archives(fetcher=fetcher)\n"
        "for i in fetcher.items:\n"
        "    print(i)\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--extension-pkg-allow-list=apt_pkg",
            "--disable=all",
            "--enable=not-an-iterable",
            "example.py",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    # "Bug still real" diagnostic: assert the FP IS present.
    assert "not-an-iterable" in output, (
        f"#7122 appears to be fixed on {sys.platform}. "
        f"Promote this test to assert the FP is ABSENT and close. Output: {output!r}"
    )

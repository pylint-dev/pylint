# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/6352

A class that subclasses ``Gtk.Window`` *and* sets at least one instance
attribute on ``self`` triggers a false ``no-member`` for inherited
members like ``add`` and ``show_all``. Drop the ``self.x = ...``
assignment and the FP disappears. This test asserts the FP is **present**
today: when CI is red, the bug is still real.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("gi", reason="PyGObject is required to reproduce #6352")


def test_pygobject_window_self_attr_triggers_no_member(tmp_path: Path) -> None:
    """``self.x = ...`` in a ``Gtk.Window`` subclass must not hide inherited members."""
    (tmp_path / "main_window.py").write_text(
        '"""Main window."""\n'
        "from typing import Tuple\n"
        "\n"
        "import gi\n"
        'gi.require_version("Gtk", "3.0")\n'
        "# pylint: disable=wrong-import-position\n"
        "from gi.repository import Gtk\n"
        "# pylint: enable=wrong-import-position\n"
        "\n"
        "\n"
        "class MainWindow(Gtk.Window):\n"
        '    """Main."""\n'
        "\n"
        "    WINDOW_SIZE: Tuple[int, int] = (500, 250)\n"
        '    INPUT_FILE_BUTTON_LABEL: str = "Choose input file"\n'
        "\n"
        "    def __init__(self, title: str):\n"
        "        super().__init__(title=title)\n"
        "        self.set_size_request(*self.WINDOW_SIZE)\n"
        "        main_box: Gtk.Box = Gtk.Box.new(\n"
        "            orientation=Gtk.Orientation.VERTICAL, spacing=10\n"
        "        )\n"
        "        self.add(main_box)\n"
        "        self.input_file_button = Gtk.Button.new(\n"
        "            label=self.INPUT_FILE_BUTTON_LABEL\n"
        "        )\n"
        "        self.show_all()\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--disable=all",
            "--enable=no-member",
            "main_window.py",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    # This is a "bug still real" diagnostic: we assert the FP IS present.
    # When this test starts to fail (i.e. no-member stops firing), the bug is fixed.
    assert "no-member" in output, (
        f"#6352 appears to be fixed (no FP emitted on {sys.platform}). "
        f"Promote this test to assert the FP is ABSENT and close. Output: {output!r}"
    )

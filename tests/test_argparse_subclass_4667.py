# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/4667

Subclassing ``argparse.ArgumentParser`` once made pylint emit ``no-member``
on ``parsed_args.logdir`` (Py3.9-specific at the time). Pylint no longer
supports Py3.9, but the inference of ``Namespace`` attributes is general
enough that we verify the FP stays gone on every supported interpreter.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_argparse_subclass_no_member_absent(tmp_path: Path) -> None:
    """Subclassing ArgumentParser must not poison Namespace attribute inference."""
    (tmp_path / "cli.py").write_text(
        '"""CLI."""\n'
        "import argparse\n"
        "\n"
        "\n"
        "class SilentArgumentParser(argparse.ArgumentParser):\n"
        '    """Silent parser."""\n'
        "\n"
        "    def error(self, message=None):\n"
        "        raise SystemExit(2)\n"
        "\n"
        "    def exit(self, status=0, message=None):\n"
        "        raise SystemExit(status)\n"
        "\n"
        "\n"
        "def parse_args(argv):\n"
        '    """Parse."""\n'
        "    parser = SilentArgumentParser()\n"
        '    parser.add_argument("--logdir", type=str, default=None)\n'
        '    parser.add_argument("name", type=str, default=None)\n'
        "    return parser.parse_args(argv)\n"
        "\n"
        "\n"
        'args = parse_args(["foo"])\n'
        "print(args.name)\n"
        "print(args.logdir)\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--disable=all",
            "--enable=no-member",
            "cli.py",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "no-member" not in output, f"#4667 regression on {sys.version}: {output!r}"

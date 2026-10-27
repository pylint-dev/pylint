# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Diagnostic for https://github.com/pylint-dev/pylint/issues/8980

When both ``azure-monitor-opentelemetry`` and
``azure-monitor-opentelemetry-exporter`` are installed (separate
distributions sharing the ``azure.monitor.opentelemetry`` namespace),
pylint used to emit ``no-name-in-module`` for the second distribution's
names. Confirm namespace-package resolution now works.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip(
    "azure.monitor.opentelemetry.exporter",
    reason="azure-monitor-opentelemetry-exporter is required to reproduce #8980",
)


def test_azure_namespace_package_resolves(tmp_path: Path) -> None:
    """Imports from the namespace-shared exporter package must resolve."""
    (tmp_path / "use.py").write_text(
        '"""Use the namespace import."""\n'
        "from azure.monitor.opentelemetry.exporter import (\n"
        "    ApplicationInsightsSampler,\n"
        "    AzureMonitorLogExporter,\n"
        "    AzureMonitorMetricExporter,\n"
        "    AzureMonitorTraceExporter,\n"
        ")\n"
        "\n"
        "print(\n"
        "    ApplicationInsightsSampler,\n"
        "    AzureMonitorLogExporter,\n"
        "    AzureMonitorMetricExporter,\n"
        "    AzureMonitorTraceExporter,\n"
        ")\n"
    )

    process = subprocess.run(
        [
            sys.executable,
            "-m",
            "pylint",
            "--disable=all",
            "--enable=no-name-in-module",
            "use.py",
        ],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    output = process.stdout + process.stderr
    assert "no-name-in-module" not in output, f"#8980 regression: {output!r}"

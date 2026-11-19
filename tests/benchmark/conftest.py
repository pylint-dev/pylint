# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Shared fixtures for the CodSpeed benchmarks.

Without ``--codspeed`` the ``benchmark`` fixture from ``pytest-codspeed`` calls
the measured function once, so every benchmark also runs as a plain test in
the normal test suite. Benchmarks over a primer project need to clone it, so
they only run when CodSpeed is measuring.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from pylint.testutils._primer import PackageToLint
from pylint.testutils.lint_module_test import PYLINTRC

HERE = Path(__file__).parent
PRIMER_PACKAGES = HERE.parent / "primer" / "packages_to_prime.json"
MINIMAL_FILE = HERE.parent / "input" / "benchmark_minimal_file.py"


def _codspeed_enabled(config: pytest.Config) -> bool:
    return bool(
        config.getoption("--codspeed") or os.environ.get("CODSPEED_ENV") is not None
    )


def _primer_package(name: str, config: pytest.Config) -> PackageToLint:
    """Clone a package from the primer at its pinned commit.

    Benchmarks reuse the primer pins, so a primer bump also moves the
    benchmark baseline: CodSpeed shows that as a change on the bump's PR.
    """
    if not _codspeed_enabled(config):
        pytest.skip("Clones a primer project, only run with --codspeed")
    packages = json.loads(PRIMER_PACKAGES.read_text(encoding="utf8"))
    package = PackageToLint(**packages[name])
    package.lazy_clone()
    return package


@pytest.fixture(scope="session")
def flask(request: pytest.FixtureRequest) -> PackageToLint:
    return _primer_package("flask", request.config)


@pytest.fixture(scope="session")
def black(request: pytest.FixtureRequest) -> PackageToLint:
    return _primer_package("black", request.config)


@pytest.fixture(scope="session")
def minimal_file() -> Path:
    return MINIMAL_FILE


@pytest.fixture(scope="session")
def many_files(tmp_path_factory: pytest.TempPathFactory) -> list[str]:
    """Distinct copies of the minimal file: pylint skips a path given twice."""
    directory = tmp_path_factory.mktemp("many_files")
    paths = []
    for i in range(100):
        path = directory / f"module_{i}.py"
        path.write_text(MINIMAL_FILE.read_text(encoding="utf8"), encoding="utf8")
        paths.append(str(path))
    return paths


_LIST_PYLINT_MODULES = """
import sys
before = set(sys.modules)
from pylint.lint import Run
from pylint.reporters import CollectingReporter
Run(sys.argv[1:], reporter=CollectingReporter(), exit=False)
for name in sorted(set(sys.modules) - before):
    top = name.partition(".")[0]
    if top not in sys.stdlib_module_names and not top.startswith("_"):
        print(name)
"""


@pytest.fixture(scope="session")
def pylint_modules() -> list[str]:
    """The modules outside the standard library loaded to lint a small file.

    Listed in a new interpreter, as this test session already imported them.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            _LIST_PYLINT_MODULES,
            f"--rcfile={PYLINTRC}",
            str(MINIMAL_FILE),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.split()

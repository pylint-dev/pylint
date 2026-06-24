# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import abc
import argparse
from pathlib import Path
from typing import TypedDict

from pylint.testutils._primer import PackageToLint
from pylint.testutils._primer.pyreverse_primer_target import PyreversePrimerTarget


class PyreverseTargetData(TypedDict):
    commit: str
    diagram: str


PyreversePrimerOutput = dict[str, PyreverseTargetData]


class PyreversePrimerCommand:
    """Base command for the pyreverse primer."""

    def __init__(
        self,
        primer_directory: Path,
        packages: dict[str, PackageToLint],
        targets: dict[str, PyreversePrimerTarget],
        config: argparse.Namespace,
    ) -> None:
        self.primer_directory = primer_directory
        self.packages = packages
        self.targets = targets
        self.config = config

    @abc.abstractmethod
    def run(self) -> None:
        pass

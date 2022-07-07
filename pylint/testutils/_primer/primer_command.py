# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import abc
import argparse
from pathlib import Path
from typing import Dict, List

from pylint.message import Message
from pylint.testutils._primer import PackageToLint

PackageMessages = Dict[str, List[Message]]


class PrimerCommand:
    """Generic primer action with required arguments."""

    def __init__(
        self,
        primer_directory: Path,
        packages: dict[str, PackageToLint],
        config: argparse.Namespace,
    ) -> None:
        self.primer_directory = primer_directory
        self.packages = packages
        self.config = config

    @abc.abstractmethod
    def run(self) -> None:
        pass

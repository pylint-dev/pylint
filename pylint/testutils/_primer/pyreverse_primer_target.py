# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PyreversePrimerTarget:
    """Single pyreverse diagram target to snapshot and compare."""

    package: str
    class_name: str
    path: str
    pyreverse_additional_args: list[str] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        return self.class_name.rsplit(".", maxsplit=1)[-1]

    @property
    def output_name(self) -> str:
        return self.class_name

    def pyreverse_args(self, output_directory: str) -> list[str]:
        return [
            "-o",
            "mmd",
            "-d",
            output_directory,
            "-c",
            self.class_name,
            "--only-classnames",
            "--no-standalone",
            *self.pyreverse_additional_args,
            self.path,
        ]

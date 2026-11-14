# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import TypedDict

from git.repo import Repo

from pylint.pyreverse.main import Run
from pylint.testutils._primer.pyreverse_primer_command import (
    PyreversePrimerCommand,
    PyreversePrimerOutput,
    PyreverseTargetData,
)


class RenderedTargetData(TypedDict):
    output_file: str
    diagram: str


class RunCommand(PyreversePrimerCommand):
    """Generate pyreverse diagrams for all configured primer targets."""

    def run(self) -> None:
        output: PyreversePrimerOutput = {}
        for target_name, target in self.targets.items():
            package = self.packages[target.package]
            local_commit = Repo(package.clone_directory).head.object.hexsha
            output[target_name] = PyreverseTargetData(
                commit=local_commit,
                **self._render_target(package.clone_directory, target_name),
            )

        path = self.primer_directory / (
            f"pyreverse_output_{'.'.join(str(i) for i in sys.version_info[:2])}_{self.config.type}.txt"
        )
        print(f"Writing result in {path}")
        with open(path, "w", encoding="utf-8") as stream:
            json.dump(output, stream)

    def _render_target(
        self, package_directory: Path, target_name: str
    ) -> RenderedTargetData:
        target = self.targets[target_name]
        current_directory = Path.cwd()
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                os.chdir(package_directory)
                exit_code = Run(target.pyreverse_args(tmpdir)).run()
            finally:
                os.chdir(current_directory)
            if exit_code != 0:
                raise RuntimeError(
                    f"Pyreverse failed for target '{target_name}' with exit code {exit_code}."
                )

            diagram_path = self._get_diagram_path(Path(tmpdir), target_name)
            with open(diagram_path, encoding="utf-8") as stream:
                return RenderedTargetData(
                    output_file=diagram_path.name,
                    diagram=stream.read(),
                )

    @staticmethod
    def _get_diagram_path(output_directory: Path, target_name: str) -> Path:
        diagram_paths = sorted(output_directory.glob("*.mmd"))
        if len(diagram_paths) != 1:
            raise RuntimeError(
                f"Expected exactly one pyreverse diagram for target '{target_name}', "
                f"got {len(diagram_paths)}."
            )
        return diagram_paths[0]

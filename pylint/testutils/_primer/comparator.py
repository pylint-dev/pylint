# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import NamedTuple

from pylint.reporters.json_reporter import JSONMessage
from pylint.testutils._primer.primer_command import (
    PackageData,
    PackageMessages,
)


class PackageDiff(NamedTuple):
    """Per-package outcome of comparing a main run against a PR run."""

    package: str
    missing: PackageData  # emitted on main but not on the PR
    new: PackageData  # emitted on the PR but not on main


class Comparator:
    """Cross-reference two primer JSON outputs and iterate over differences."""

    def __init__(self, main_data: PackageMessages, pr_data: PackageMessages) -> None:
        self._main_data = main_data
        self._pr_data = pr_data

    @staticmethod
    def from_json(
        base_file: Path | str, new_file: Path | str, batches: int | None = None
    ) -> Comparator:
        """Build a Comparator from JSON file paths, handling batched runs."""
        main_data: PackageMessages
        pr_data: PackageMessages
        if batches is None:
            main_data = Comparator._load_json(base_file)
            pr_data = Comparator._load_json(new_file)
        else:
            main_data = {}
            pr_data = {}
            for idx in range(batches):
                suffix = f"batch{idx}"
                main_data.update(
                    Comparator._load_json(str(base_file).replace("BATCHIDX", suffix))
                )
                pr_data.update(
                    Comparator._load_json(str(new_file).replace("BATCHIDX", suffix))
                )
        return Comparator(main_data, pr_data)

    def __iter__(self) -> Iterator[PackageDiff]:
        main_data = self._main_data
        pr_data = self._pr_data

        missing_messages: PackageMessages = {}
        for package, data in main_data.items():
            package_missing_messages: list[JSONMessage] = []
            for message in data["messages"]:
                try:
                    pr_data[package]["messages"].remove(message)
                except ValueError:
                    package_missing_messages.append(message)
            missing_messages[package] = PackageData(
                commit=pr_data[package]["commit"],
                messages=package_missing_messages,
            )

        for package, pkg_missing in missing_messages.items():
            new_messages = pr_data[package]
            if not pkg_missing["messages"] and not new_messages["messages"]:
                continue
            yield PackageDiff(package, pkg_missing, new_messages)

    @staticmethod
    def _load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result

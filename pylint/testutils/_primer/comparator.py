# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path

from pylint.reporters.json_reporter import OldJsonExport
from pylint.testutils._primer.primer_command import (
    PackageData,
    PackageMessages,
)


class Comparator:
    def __init__(
        self, base_file: str, new_file: str, batches: int | None = None
    ) -> None:
        self._base_file = base_file
        self._new_file = new_file
        self._batches = batches

    def __iter__(self) -> Generator[tuple[str, PackageData, PackageData]]:
        main_data: PackageMessages
        if self._batches is None:
            main_data = self._load_json(self._base_file)
            pr_data = self._load_json(self._new_file)
        else:
            main_data = {}
            pr_data = {}
            for idx in range(self._batches):
                main_data.update(
                    self._load_json(
                        self._base_file.replace("BATCHIDX", "batch" + str(idx))
                    )
                )
                pr_data.update(
                    self._load_json(
                        self._new_file.replace("BATCHIDX", "batch" + str(idx))
                    )
                )

        missing_messages: PackageMessages = {}
        for package, data in main_data.items():
            package_missing_messages: list[OldJsonExport] = []
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
            yield package, pkg_missing, new_messages

    @staticmethod
    def _load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result

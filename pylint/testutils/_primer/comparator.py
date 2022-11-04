# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections.abc import Generator
from pathlib import Path

from pylint.testutils._primer.primer_command import Messages, PackageMessages


class Comparator:
    def __init__(self, main_json: Path, pr_json: Path):
        main_messages = self._load_json(main_json)
        self.pr_messages = self._load_json(pr_json)
        self.missing_messages: PackageMessages = {}
        for package, messages in main_messages.items():
            self.missing_messages[package] = []
            for message in messages:
                try:
                    self.pr_messages[package].remove(message)
                except ValueError:
                    self.missing_messages[package].append(message)

    def __iter__(
        self,
    ) -> Generator[tuple[str, Messages, Messages], None, None]:
        for package, missing_messages in self.missing_messages.items():
            new_messages = self.pr_messages[package]
            if not missing_messages and not new_messages:
                print(f"PRIMER: No changes in {package}.")
                continue
            yield package, missing_messages, new_messages

    @staticmethod
    def _load_json(file_path: Path | str) -> PackageMessages:
        with open(file_path, encoding="utf-8") as f:
            result: PackageMessages = json.load(f)
        return result

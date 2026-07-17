# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""SARIF reporter."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pylint.__pkginfo__ import __version__
from pylint.reporters.base_reporter import BaseReporter

if TYPE_CHECKING:
    from pylint.lint.pylinter import PyLinter
    from pylint.message import Message
    from pylint.reporters.ureports.nodes import Section

# SARIF 2.1.0 result levels
_CATEGORY_TO_LEVEL = {
    "fatal": "error",
    "error": "error",
    "warning": "warning",
    "refactor": "note",
    "convention": "note",
    "info": "note",
}

_MESSAGE_DOC_BASE = (
    "https://pylint.readthedocs.io/en/latest/user_guide/messages"
)


def _path_to_uri(path: str) -> str:
    """Return a SARIF-compatible URI for *path*."""
    pathlib_path = Path(path)
    if pathlib_path.is_absolute():
        return pathlib_path.as_uri()
    return path.replace("\\", "/")


def _region_from_message(message: Message) -> dict[str, int]:
    """Build a SARIF region (1-based line/column) from a pylint message."""
    region: dict[str, int] = {
        "startLine": max(message.line, 1),
        # pylint columns are 0-based; SARIF columns are 1-based
        "startColumn": message.column + 1,
    }
    if message.end_line is not None:
        region["endLine"] = max(message.end_line, 1)
    if message.end_column is not None:
        region["endColumn"] = message.end_column + 1
    return region


class SARIFReporter(BaseReporter):
    """Report messages in SARIF 2.1.0 format."""

    name = "sarif"
    extension = "sarif"

    def display_reports(self, layout: Section) -> None:
        """Don't do anything in this reporter."""

    def _display(self, layout: Section) -> None:
        """Do nothing."""

    def display_messages(self, layout: Section | None) -> None:
        """Emit a SARIF log containing all collected messages."""
        print(json.dumps(self.serialize(), indent=2), file=self.out)

    def serialize(self) -> dict[str, Any]:
        """Serialize collected messages to a SARIF 2.1.0 object."""
        rules_by_id: dict[str, dict[str, Any]] = {}
        results: list[dict[str, Any]] = []

        for message in self.messages:
            if message.msg_id not in rules_by_id:
                rules_by_id[message.msg_id] = self._rule_from_message(message)
            results.append(self._result_from_message(message))

        return {
            "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
            "version": "2.1.0",
            "runs": [
                {
                    "tool": {
                        "driver": {
                            "name": "pylint",
                            "version": __version__,
                            "informationUri": "https://github.com/pylint-dev/pylint",
                            "rules": list(rules_by_id.values()),
                        }
                    },
                    "results": results,
                }
            ],
        }

    def _rule_from_message(self, message: Message) -> dict[str, Any]:
        description = message.symbol
        try:
            definitions = self.linter.msgs_store.get_message_definitions(
                message.msg_id
            )
            if definitions and definitions[0].description:
                description = definitions[0].description
        except Exception:  # pylint: disable=broad-except
            pass

        return {
            "id": message.msg_id,
            "name": message.symbol,
            "shortDescription": {"text": message.symbol},
            "fullDescription": {"text": description},
            "helpUri": (
                f"{_MESSAGE_DOC_BASE}/{message.category}/{message.symbol}.html"
            ),
            "properties": {"category": message.category},
        }

    @staticmethod
    def _result_from_message(message: Message) -> dict[str, Any]:
        result: dict[str, Any] = {
            "ruleId": message.msg_id,
            "level": _CATEGORY_TO_LEVEL.get(message.category, "warning"),
            "message": {"text": message.msg or ""},
            "locations": [
                {
                    "physicalLocation": {
                        "artifactLocation": {"uri": _path_to_uri(message.path)},
                        "region": _region_from_message(message),
                    }
                }
            ],
            "properties": {
                "category": message.category,
                "symbol": message.symbol,
                "confidence": message.confidence.name,
                "module": message.module,
                "obj": message.obj,
            },
        }
        return result


def register(linter: PyLinter) -> None:
    linter.register_reporter(SARIFReporter)

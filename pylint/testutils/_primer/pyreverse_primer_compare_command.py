# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

import json
from collections.abc import Iterator
from difflib import unified_diff
from pathlib import Path

from pylint.testutils._primer.pyreverse_primer_command import (
    PyreversePrimerCommand,
    PyreversePrimerOutput,
    PyreverseTargetData,
)

MAX_GITHUB_COMMENT_LENGTH = 65536
COMMENT_MARKER = "<!-- pyreverse-primer-comment -->\n"


class CompareCommand(PyreversePrimerCommand):
    """Compare pyreverse primer outputs and render a GitHub comment."""

    def run(self) -> None:
        base_data = self._load_json(self.config.base_file)
        new_data = self._load_json(self.config.new_file)
        comment = self._create_comment(base_data, new_data)
        with open(
            self.primer_directory / "comment.txt", "w", encoding="utf-8"
        ) as stream:
            stream.write(comment)

    def _create_comment(
        self, base_data: PyreversePrimerOutput, new_data: PyreversePrimerOutput
    ) -> str:
        comment = ""
        for target_name, base_target_data, new_target_data in self._iter_changes(
            base_data, new_data
        ):
            if len(comment) >= MAX_GITHUB_COMMENT_LENGTH:
                break
            comment += self._create_comment_for_target(
                target_name, base_target_data, new_target_data
            )

        comment = (
            COMMENT_MARKER
            + f"🤖 **Effect of this PR on tracked pyreverse diagrams:** 🤖\n\n{comment}"
            if comment
            else (
                COMMENT_MARKER
                + "🤖 According to the pyreverse primer, this change has **no effect** on"
                " the tracked diagrams. 🤖🎉\n\n"
            )
        )
        return self._truncate_comment(comment)

    def _create_comment_for_target(
        self,
        target_name: str,
        base_target_data: PyreverseTargetData,
        new_target_data: PyreverseTargetData,
    ) -> str:
        target = self.targets[target_name]
        package = self.packages[target.package]
        diff = self._diagram_diff(
            base_target_data["diagram"],
            new_target_data["diagram"],
        )
        return (
            f"**Effect on `{target.display_name}` in [{target.package}]({package.url}):**\n\n"
            "<details>\n<summary>Diagram diff</summary>\n\n"
            f"```diff\n{diff}```\n"
            "</details>\n\n"
            "<details>\n<summary>Rendered diagram</summary>\n\n"
            f"```mermaid\n{new_target_data['diagram'].rstrip()}\n```\n"
            "</details>\n\n"
        )

    def _truncate_comment(self, comment: str) -> str:
        hash_information = (
            f"*This comment was generated for commit {self.config.commit}*"
        )
        if len(comment) + len(hash_information) >= MAX_GITHUB_COMMENT_LENGTH:
            truncation_information = (
                "*This comment was truncated because GitHub allows only"
                f" {MAX_GITHUB_COMMENT_LENGTH} characters in a comment.*"
            )
            suffix = f"\n{truncation_information}\n\n"
            closing_tag = "</details>\n"
            max_len = (
                MAX_GITHUB_COMMENT_LENGTH
                - len(hash_information)
                - len(suffix)
                - len(closing_tag)
            )
            cut_point = comment.rfind(" ", 0, max_len - 10)
            if cut_point > 0:
                comment = comment[:cut_point] + "...\n"
            else:
                comment = comment[: max_len - 10] + "...\n"
            if comment.count("<details>") > comment.count("</details>"):
                comment += closing_tag
            comment += suffix
        comment += hash_information
        return comment

    @staticmethod
    def _diagram_diff(base_diagram: str, new_diagram: str) -> str:
        return (
            "\n".join(
                unified_diff(
                    base_diagram.splitlines(),
                    new_diagram.splitlines(),
                    fromfile="main",
                    tofile="pr",
                    lineterm="",
                )
            )
            + "\n"
        )

    @staticmethod
    def _iter_changes(
        base_data: PyreversePrimerOutput,
        new_data: PyreversePrimerOutput,
    ) -> Iterator[tuple[str, PyreverseTargetData, PyreverseTargetData]]:
        for target_name, base_target_data in base_data.items():
            new_target_data = new_data[target_name]
            if base_target_data["diagram"] == new_target_data["diagram"]:
                continue
            yield target_name, base_target_data, new_target_data

    @staticmethod
    def _load_json(file_path: Path | str) -> PyreversePrimerOutput:
        with open(file_path, encoding="utf-8") as stream:
            result: PyreversePrimerOutput = json.load(stream)
        return result

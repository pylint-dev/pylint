# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Small script to fix various issues with the documentation. Used by pre-commit."""

from __future__ import annotations

import argparse
import re
import sys

INVALID_CODE_BLOCK_PATTERN = (
    r"(?<=\s`)([\w\-\.\(\)\=]+\s{0,1}[\w\-\.\(\)\=]*)(?=`[,\.]{0,1}\s|$)"
)

# TODO: 2.16.0: Upgrade script for change in changelog
DEFAULT_CHANGELOG = "ChangeLog"
DEFAULT_SUBTITLE_PREFIX = "What's New in"


def fix_inline_code_blocks(file_content: str) -> str:
    """Use double quotes for code blocks. RST style.

    Example:
        `hello-world` -> ``hello-world``
    """
    pattern = re.compile(INVALID_CODE_BLOCK_PATTERN)
    return pattern.sub(r"`\g<0>`", file_content)


def changelog_insert_empty_lines(file_content: str, subtitle_text: str) -> str:
    """Insert up to two empty lines before `What's New` entry in ChangeLog."""
    lines = file_content.split("\n")
    subtitle_count = 0
    for i, line in enumerate(lines):
        if line.startswith(subtitle_text):
            subtitle_count += 1
            if subtitle_count == 1 or i < 2 or not lines[i - 1] and not lines[i - 2]:
                continue
            lines.insert(i, "")
    return "\n".join(lines)


class CustomHelpFormatter(argparse.HelpFormatter):
    def __init__(
        self,
        prog: str,
        indent_increment: int = 2,
        max_help_position: int = 24,
        width: int | None = None,
    ) -> None:
        max_help_position = 40
        super().__init__(
            prog,
            indent_increment=indent_increment,
            max_help_position=max_help_position,
            width=width,
        )


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(formatter_class=CustomHelpFormatter)
    parser.add_argument(
        "--changelog",
        metavar="file",
        default=DEFAULT_CHANGELOG,
        help="Changelog filename (default: '%(default)s')",
    )
    parser.add_argument(
        "--subtitle-prefix",
        metavar="prefix",
        default=DEFAULT_SUBTITLE_PREFIX,
        help="Subtitle prefix (default: '%(default)s')",
    )
    parser.add_argument(
        "filenames",
        nargs="*",
        metavar="FILES",
        help="File names to modify",
    )
    args = parser.parse_args(argv)

    return_value: int = 0
    for file_name in args.filenames:
        with open(file_name, encoding="utf-8") as fp:
            original_content = fp.read()
        content = original_content
        # Modify files
        content = fix_inline_code_blocks(content)
        if file_name == args.changelog:
            content = changelog_insert_empty_lines(content, args.subtitle_prefix)
        # If modified, write changes and eventually return 1
        if original_content != content:
            with open(file_name, "w", encoding="utf-8") as fp:
                fp.write(content)
            return_value |= 1
    return return_value


if __name__ == "__main__":
    sys.exit(main())

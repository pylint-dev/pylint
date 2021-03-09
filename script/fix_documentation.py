"""Small script to fix various issues with the documentation. Used by pre-commit."""

import argparse
import re
import sys
from typing import List, Union

INVALID_CODE_BLOCK_PATTERN = (
    r"(?<=\s`)([\w\-\.\(\)\=]+\s{0,1}[\w\-\.\(\)\=]*)(?=`[,\.]{0,1}\s|$)"
)

FILE_CHANGELOG = "ChangeLog"
CHANGELOG_WHATS_NEW_PREFIX = "What's New in Pylint"


def fix_inline_code_blocks(file_content: str) -> str:
    """Use double quotes for code blocks. RST style.

    Example:
        `hello-world` -> ``hello-world``
    """
    pattern = re.compile(INVALID_CODE_BLOCK_PATTERN)
    return pattern.sub(r"`\g<0>`", file_content)


def changelog_insert_empty_lines(file_content: str) -> str:
    """Insert up to two empty lines before `What's New` entry in ChangeLog"""
    lines = file_content.split("\n")
    version_count = 0
    for i, line in enumerate(lines):
        if line.startswith(CHANGELOG_WHATS_NEW_PREFIX):
            version_count += 1
            if version_count == 1 or i < 2 or lines[i - 1] == "" and lines[i - 2] == "":
                continue
            lines.insert(i, "")
    return "\n".join(lines)


def main(argv: Union[List[str], None] = None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        metavar="FILES",
        help="File names to modify",
    )
    args = parser.parse_args(argv)

    return_value: int = 0
    for file_name in args.filenames:
        with open(file_name) as fp:
            orignal_content = fp.read()
        content = orignal_content
        # Modify files
        content = fix_inline_code_blocks(content)
        if file_name == FILE_CHANGELOG:
            content = changelog_insert_empty_lines(content)
        # If modified, write changes and eventually return 1
        if orignal_content != content:
            with open(file_name, "w") as fp:
                fp.write(content)
            return_value |= 1
    return return_value


if __name__ == "__main__":
    sys.exit(main())

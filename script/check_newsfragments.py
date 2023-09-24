# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Small script to check the formatting of news fragments for towncrier.
Used by pre-commit.
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path
from re import Pattern

VALID_ISSUES_KEYWORDS = [
    "Refs",
    "Closes",
    "Follow-up in",
    "Fixes part of",
]
VALID_FILE_TYPE = frozenset(
    [
        "breaking",
        "user_action",
        "feature",
        "new_check",
        "removed_check",
        "extension",
        "false_positive",
        "false_negative",
        "bugfix",
        "other",
        "internal",
        "performance",
    ]
)
ISSUES_KEYWORDS = "|".join(VALID_ISSUES_KEYWORDS)
VALID_CHANGELOG_PATTERN = (
    rf"(?P<description>(.*\n)*(.*\.\n))\n(?P<ref>({ISSUES_KEYWORDS})"
    r" (pylint-dev/astroid)?#(?P<issue>\d+))"
)
VALID_CHANGELOG_COMPILED_PATTERN: Pattern[str] = re.compile(
    VALID_CHANGELOG_PATTERN, flags=re.MULTILINE
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        metavar="FILES",
        help="File names to check",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args(argv)
    is_valid = True
    for filename in args.filenames:
        is_valid &= check_file(Path(filename), args.verbose)
    return 0 if is_valid else 1


def check_file(file: Path, verbose: bool) -> bool:
    """Check that a file contains a valid changelog entry."""
    with open(file, encoding="utf8") as f:
        content = f.read()
    match = VALID_CHANGELOG_COMPILED_PATTERN.match(content)
    if match:
        issue = match.group("issue")
        if file.stem != issue:
            echo(
                f"{file} must be named '{issue}.<fragmenttype>', after the issue it references."
            )
            return False
        if not any(file.suffix.endswith(t) for t in VALID_FILE_TYPE):
            suggestions = difflib.get_close_matches(file.suffix, VALID_FILE_TYPE)
            if suggestions:
                multiple_suggestions = "', '".join(f"{issue}.{s}" for s in suggestions)
                suggestion = f"should probably be named '{multiple_suggestions}'"
            else:
                multiple_suggestions = "', '".join(
                    f"{issue}.{s}" for s in VALID_FILE_TYPE
                )
                suggestion = f"must be named one of '{multiple_suggestions}'"
            echo(f"{file} {suggestion} instead.")
            return False
        if verbose:
            echo(f"Checked '{file}': LGTM 🤖👍")
        return True
    echo(
        f"""\
{file}: does not respect the standard format 🤖👎

The standard format is:

<one or more line of text ending with a '.'>
<one blank line>
<issue reference> #<issuenumber>

Where <issue reference> can be one of: {', '.join(VALID_ISSUES_KEYWORDS)}

The regex used is '{VALID_CHANGELOG_COMPILED_PATTERN}'.

For example:

``pylint.x.y`` is now a private API.

Refs #1234
"""
    )
    return False


def echo(msg: str) -> None:
    # To support non-UTF-8 environments like Windows, we need
    # to explicitly encode the message instead of using plain print()
    sys.stdout.buffer.write(f"{msg}\n".encode())


if __name__ == "__main__":
    sys.exit(main())

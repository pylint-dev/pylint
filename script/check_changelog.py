# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

"""Small script to check the changelog. Used by 'changelog.yml' and pre-commit.

If no issue number is provided we only check that proper formatting is respected."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator
from pathlib import Path
from re import Pattern

ISSUE_NUMBER_PATTERN = re.compile(r"#\d{1,5}")
VALID_CHANGELOG_PATTERN: Pattern[str] = re.compile(
    r"(\*\s[\S[\n ]+?]*\n\n\s\s(Refs|Closes|Follow-up in|Fixes part of)) (PyCQA/astroid)?#\d{1,5}"
)
VALID_ISSUE_NUMBER_PATTERN: Pattern[str] = re.compile(r"\*[\S\s]*?#\d{1,5}")
DOC_PATH = (Path(__file__).parent / "../doc/").resolve()
PATH_TO_WHATSNEW = DOC_PATH / "whatsnew"
UNCHECKED_VERSION = [
    # Not checking version prior to 1.0.0 because the issues referenced are a mix
    # between Logilab internal issue and Bitbucket. It's hard to tell, it's
    # inaccessible for Logilab and often dead links for Bitbucket anyway.
    # Not very useful generally, unless you're an open source historian.
    "0.x",
    # Too much Bitbucket issues in this one :
    "1.0",
    "1.1",
    "1.2",
]

NO_CHECK_REQUIRED_FILES = {
    "index.rst",
    "full_changelog_explanation.rst",
    "summary_explanation.rst",
}


def sorted_whatsnew(verbose: bool) -> Iterator[Path]:
    """Return the whats-new in the 'right' numerical order ('9' before '10')"""
    numeric_whatsnew = {}
    for file in PATH_TO_WHATSNEW.glob("**/*"):
        relpath_file = file.relative_to(DOC_PATH)
        if file.is_dir():
            if verbose:
                print(f"I don't care about '{relpath_file}', it's a directory : 🤖🤷")
            continue
        if file.name in NO_CHECK_REQUIRED_FILES:
            if verbose:
                print(
                    f"I don't care about '{relpath_file}' it's in 'NO_CHECK_REQUIRED_FILES' : 🤖🤷"
                )
            continue
        version = (
            file.parents[0].name if file.stem in {"summary", "full"} else file.stem
        )
        if any(version == x for x in UNCHECKED_VERSION):
            if verbose:
                print(
                    f"I don't care about '{relpath_file}' {version} is in UNCHECKED_VERSION : 🤖🤷"
                )
            continue
        if verbose:
            print(f"I'm going to check '{relpath_file}' 🤖")
        num = tuple(int(x) for x in (version.split(".")))
        numeric_whatsnew[num] = file
    for num in sorted(numeric_whatsnew):
        yield numeric_whatsnew[num]


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--issue-number",
        type=int,
        default=0,
        help="The issue we expect to find in the changelog.",
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    args = parser.parse_args(argv)
    verbose = args.verbose
    is_valid = True
    for file in sorted_whatsnew(verbose):
        if not check_file(file, verbose):
            is_valid = False
    return 0 if is_valid else 1


def check_file(file: Path, verbose: bool) -> bool:
    """Check that a file contain valid change-log's entries."""
    with open(file, encoding="utf8") as f:
        content = f.read()
    valid_full_descriptions = VALID_CHANGELOG_PATTERN.findall(content)
    result = len(valid_full_descriptions)
    contain_issue_number_descriptions = VALID_ISSUE_NUMBER_PATTERN.findall(content)
    expected = len(contain_issue_number_descriptions)
    if result != expected:
        return create_detailed_fail_message(
            file, contain_issue_number_descriptions, valid_full_descriptions
        )
    if verbose:
        relpath_file = file.relative_to(DOC_PATH)
        print(f"Checked '{relpath_file}' : LGTM 🤖👍")
    return True


def create_detailed_fail_message(
    file_name: Path,
    contain_issue_number_descriptions: list,
    valid_full_descriptions: list,
) -> bool:
    is_valid = True
    for issue_number_description in contain_issue_number_descriptions:
        if not any(v[0] in issue_number_description for v in valid_full_descriptions):
            is_valid = False
            issue_number = ISSUE_NUMBER_PATTERN.findall(issue_number_description)[0]
            print(
                f"{file_name}: {issue_number}'s description is not on one line, or "
                "does not respect the standard format 🤖👎"
            )
    return is_valid


if __name__ == "__main__":
    sys.exit(main())

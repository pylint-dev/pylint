# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""This script updates towncrier.toml and creates a new newsfile and intermediate
folders if necessary.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from subprocess import check_call

NEWSFILE_PATTERN = re.compile(r"doc/whatsnew/\d/\d.\d+/index\.rst")
NEWSFILE_PATH = "doc/whatsnew/{major}/{major}.{minor}/index.rst"
TOWNCRIER_CONFIG_FILE = Path("towncrier.toml")
# 'major.minor.patch' followed by an optional pre-release suffix, written either the
# semantic versioning way ('4.1.0-dev0') or the PEP 440 one ('3.3.5a0'). Pylint has
# used both.
VERSION_PATTERN = (
    r"(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?P<suffix>-?[a-zA-Z][0-9a-zA-Z.-]*)?"
)
NEW_VERSION_PATTERN = re.compile(rf"^{VERSION_PATTERN}$")
# Between releases towncrier.toml holds a pre-release version, so the suffix has to
# be part of the pattern. Matching only 'major.minor.patch' left the version
# untouched, and towncrier then titled the new section with the stale version.
TOWNCRIER_VERSION_PATTERN = re.compile(rf"version = \"{VERSION_PATTERN}\"")
# The issues a fragment refers to, like 'Closes #123', possibly in the astroid repository
ISSUE_PATTERN = re.compile(r"(?<![\w`/#<])(pylint-dev/astroid)?#(\d+)\b")

NEWSFILE_CONTENT_TEMPLATE = """
***************************
 What's New in Pylint {major}.{minor}
***************************

.. toctree::
   :maxdepth: 2

:Release:{major}.{minor}
:Date: TBA

Summary -- Release highlights
=============================


.. towncrier release notes start
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="The new version to set")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Just show what would be done, don't write anything",
    )
    args = parser.parse_args()

    if "dev" in args.version:
        print("'-devXY' will be cut from version in towncrier.toml")
    match = NEW_VERSION_PATTERN.match(args.version)
    if not match:
        print(
            "Fatal error - new version did not match the "
            "expected format (major.minor.patch[suffix]). Abort!"
        )
        return
    major, minor, patch = match["major"], match["minor"], match["patch"]
    suffix = match["suffix"]
    new_version = f"{major}.{minor}.{patch}"

    new_newsfile = NEWSFILE_PATH.format(major=major, minor=minor)
    create_new_newsfile_if_necessary(new_newsfile, major, minor, args.dry_run)
    patch_towncrier_toml(new_newsfile, new_version, args.dry_run)
    build_changelog(suffix, args.dry_run)
    if not suffix and not args.dry_run:
        link_issues(Path(new_newsfile), new_version)


def create_new_newsfile_if_necessary(
    new_newsfile: str, major: str, minor: str, dry_run: bool
) -> None:
    new_newsfile_path = Path(new_newsfile)
    if new_newsfile_path.exists():
        return

    # create new file and add boiler plate content
    if dry_run:
        print(
            f"Dry run enabled - would create file {new_newsfile} "
            "and intermediate folders"
        )
        return

    print("Creating new newsfile:", new_newsfile)
    new_newsfile_path.parent.mkdir(parents=True, exist_ok=True)
    new_newsfile_path.touch()
    new_newsfile_path.write_text(
        NEWSFILE_CONTENT_TEMPLATE.format(major=major, minor=minor),
        encoding="utf8",
    )

    # tbump does not add and commit new files, so we add it ourselves
    print("Adding new newsfile to git")
    check_call(["git", "add", new_newsfile])

    # List it first in the table of contents of the major version
    major_index = Path(f"doc/whatsnew/{major}/index.rst")
    content = major_index.read_text(encoding="utf8")
    first_entry = re.search(rf"^   {major}\.\d+/index$", content, flags=re.MULTILINE)
    assert first_entry, f"No '{major}.x/index' entry in the toctree of {major_index}"
    position = first_entry.start()
    major_index.write_text(
        f"{content[:position]}   {major}.{minor}/index\n{content[position:]}",
        encoding="utf8",
    )


def patch_towncrier_toml(new_newsfile: str, version: str, dry_run: bool) -> None:
    file_content = TOWNCRIER_CONFIG_FILE.read_text(encoding="utf-8")
    if not TOWNCRIER_VERSION_PATTERN.search(file_content):
        raise ValueError(
            f"Could not find the version to replace in {TOWNCRIER_CONFIG_FILE}. "
            "Without it towncrier would use a stale version in the changelog title."
        )
    patched_newsfile_path = NEWSFILE_PATTERN.sub(new_newsfile, file_content)
    new_file_content = TOWNCRIER_VERSION_PATTERN.sub(
        f'version = "{version}"', patched_newsfile_path
    )
    if dry_run:
        print("Dry run enabled - this is what I would write:\n")
        print(new_file_content)
        return
    TOWNCRIER_CONFIG_FILE.write_text(new_file_content, encoding="utf-8")


def build_changelog(suffix: str | None, dry_run: bool) -> None:
    if suffix:
        print("Not a release version, skipping changelog generation")
        return

    if dry_run:
        print("Dry run enabled - not building changelog")
        return

    print("Building changelog")
    check_call(["towncrier", "build", "--yes"])


def link_issues(newsfile: Path, version: str) -> None:
    """Link every issue of the new changelog section, towncrier only links the one
    in the name of the fragment.
    """
    content = newsfile.read_text(encoding="utf8")
    start = content.index(f"What's new in Pylint {version}?")
    end = content.find("What's new in Pylint ", start + 1)
    end = len(content) if end == -1 else end
    section = ISSUE_PATTERN.sub(
        lambda m: f"`{m[0]} <https://github.com/"
        f"{m[1] or 'pylint-dev/pylint'}/issues/{m[2]}>`__",
        content[start:end],
    )
    newsfile.write_text(content[:start] + section + content[end:], encoding="utf8")


if __name__ == "__main__":
    main()

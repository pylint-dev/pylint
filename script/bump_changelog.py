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
TOWNCRIER_VERSION_PATTERN = re.compile(r"version = \"(\d+\.\d+\.\d+)\"")

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
    match = re.match(
        r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(-?\w+\d*)*", args.version
    )
    if not match:
        print(
            "Fatal error - new version did not match the "
            "expected format (major.minor.patch[.*]). Abort!"
        )
        return
    major, minor, patch, suffix = match.groups()
    new_version = f"{major}.{minor}.{patch}"

    new_newsfile = NEWSFILE_PATH.format(major=major, minor=minor)
    create_new_newsfile_if_necessary(new_newsfile, major, minor, args.dry_run)
    patch_towncrier_toml(new_newsfile, new_version, args.dry_run)
    build_changelog(suffix, args.dry_run)


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


def patch_towncrier_toml(new_newsfile: str, version: str, dry_run: bool) -> None:
    file_content = TOWNCRIER_CONFIG_FILE.read_text(encoding="utf-8")
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


if __name__ == "__main__":
    main()

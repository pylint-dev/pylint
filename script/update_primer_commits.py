# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Update the pinned commit hashes in packages_to_prime.json to the latest
remote HEAD of each package's branch.

Called automatically by tbump before a release commit.
"""

from __future__ import annotations

import json
from pathlib import Path

from git.cmd import Git

PACKAGES_FILE = (
    Path(__file__).resolve().parent.parent / "tests/primer/packages_to_prime.json"
)


def main() -> None:
    text = PACKAGES_FILE.read_text(encoding="utf-8")
    packages = json.loads(text)

    for name, data in packages.items():
        old = data["commit"]
        sha = Git().ls_remote(data["url"], data["branch"]).split("\t")[0]
        if sha != old:
            print(f"  {name}: {old[:12]} -> {sha[:12]}")
            text = text.replace(old, sha)
        else:
            print(f"  {name}: up to date ({sha[:12]})")

    PACKAGES_FILE.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()

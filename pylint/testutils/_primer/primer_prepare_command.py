# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt
from __future__ import annotations

import sys

from git.repo import Repo

from pylint.testutils._primer.primer_command import PrimerCommand


class PrepareCommand(PrimerCommand):
    def run(self) -> None:
        commit_string = ""
        version_string = ".".join(str(x) for x in sys.version_info[:2])
        # Shorten the SHA to avoid exceeding GitHub's 512 char ceiling
        if self.config.clone:
            for package, data in self.packages.items():
                local_commit = data.lazy_clone()
                print(f"Cloned '{package}' at commit '{local_commit}'.")
                commit_string += local_commit[:8] + "_"
        elif self.config.check:
            for package, data in self.packages.items():
                local_commit = Repo(data.clone_directory).head.object.hexsha
                print(f"Found '{package}' at commit '{local_commit}'.")
                commit_string += local_commit[:8] + "_"
        elif self.config.make_commit_string:
            # Use the pinned commits so that runs which only differ by upstream
            # branch tips share the same cache (and thus the same on-disk file
            # order, which message positions and inference depend on).
            for package, data in self.packages.items():
                print(f"'{package}' is pinned to commit '{data.commit[:8]}'.")
                commit_string += data.commit[:8] + "_"
        elif self.config.read_commit_string:
            with open(
                self.primer_directory / f"commit_string_{version_string}.txt",
                encoding="utf-8",
            ) as f:
                print(f.read())
        if commit_string:
            with open(
                self.primer_directory / f"commit_string_{version_string}.txt",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(commit_string)

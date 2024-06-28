"""
Temporary file until we drop python 3.8
See https://github.com/pylint-dev/pylint/issues/9751
Please reunite with used_before_assignment.py at this point
"""

# pylint: disable=missing-docstring

import sys
from typing import NoReturn


class PlatformChecks:
    """https://github.com/pylint-dev/pylint/issues/9674"""
    def skip(self, msg) -> NoReturn:
        raise Exception(msg)  # pylint: disable=broad-exception-raised

    def print_platform_specific_command(self):
        if sys.platform == "linux":
            cmd = "ls"
        elif sys.platform == "win32":
            cmd = "dir"
        else:
            self.skip("only runs on Linux/Windows")

        print(cmd)

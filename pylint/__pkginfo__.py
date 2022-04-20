# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

__version__ = "2.14.0-dev0"


def get_numversion_from_version(v: str) -> tuple[int, int, int]:
    """Kept for compatibility reason.

    See https://github.com/PyCQA/pylint/issues/4399
    https://github.com/PyCQA/pylint/issues/4420,
    """
    v = v.replace("pylint-", "")
    version = []
    for n in v.split(".")[0:3]:
        try:
            version.append(int(n))
        except ValueError:
            num = ""
            for c in n:
                if c.isdigit():
                    num += c
                else:
                    break
            try:
                version.append(int(num))
            except ValueError:
                version.append(0)
    while len(version) != 3:
        version.append(0)

    return tuple(version)  # type: ignore[return-value] # mypy can't infer the length


numversion = get_numversion_from_version(__version__)

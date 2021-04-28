# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/LICENSE
from typing import Tuple

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution("pylint").version
except DistributionNotFound:
    __version__ = "2.8.2+"


def get_numversion_from_version(v: str) -> Tuple:
    """Kept for compatibility reason

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
            version.append(int(num))
    return tuple(version)


numversion = get_numversion_from_version(__version__)

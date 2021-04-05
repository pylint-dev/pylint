# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from pathlib import Path
from typing import Any, Dict

from setuptools import setup

HERE = Path(__file__).parent

__pkginfo__: Dict[str, Any] = {}
with open(HERE / "pylint/__pkginfo__.py", encoding="UTF-8") as f:
    exec(f.read(), __pkginfo__)  # pylint: disable=exec-used

if __name__ == "__main__":
    setup(version=__pkginfo__["__version__"])

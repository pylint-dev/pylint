# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from pathlib import Path
from typing import Any, Dict

from setuptools import setup

HERE = Path(__file__).parent

__pkginfo__: Dict[str, Any] = {}
with open(HERE / "pylint/__pkginfo__.py", encoding="UTF-8") as f:
    exec(f.read(), __pkginfo__)  # pylint: disable=exec-used

with open(HERE / "requirements_docs.txt", encoding="UTF-8") as f:
    doc_extra_requires = f.readlines()

with open(HERE / "requirements_test_min.txt", encoding="UTF-8") as f:
    test_requires = f.readlines()

DEV_REQUIREMENTS_FILES = ["requirements_test.txt", "requirements_test_pre_commit.txt"]
dev_extra_requires = doc_extra_requires + test_requires
for requirement_file in DEV_REQUIREMENTS_FILES:
    with open(HERE / requirement_file, encoding="UTF-8") as f:
        dev_extra_requires += [
            line for line in f.readlines() if not line.startswith("-r")
        ]


if __name__ == "__main__":
    setup(
        version=__pkginfo__["__version__"],
        tests_require=test_requires,
        extras_require={
            ':sys_platform=="win32"': ["colorama"],
            "docs": doc_extra_requires,
            "dev": dev_extra_requires,
        },
    )

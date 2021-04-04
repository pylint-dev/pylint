# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

from pathlib import Path
from typing import Any, Dict

import setuptools

HERE = Path(__file__).parent

__pkginfo__: Dict[str, Any] = {}
with open(HERE / "pylint/__pkginfo__.py", encoding="UTF-8") as f:
    exec(f.read(), __pkginfo__)  # pylint: disable=exec-used
with open(HERE / "README.rst", encoding="UTF-8") as f:
    long_description = f.read()
with open(HERE / "requirements_docs.txt", encoding="UTF-8") as f:
    doc_extra_requires = f.read()


setuptools.setup(
    name="pylint",
    version=__pkginfo__["version"],
    license=__pkginfo__["license"],
    description=__pkginfo__["description"],
    long_description=long_description,
    author=__pkginfo__["author"],
    author_email=__pkginfo__["author_email"],
    url=__pkginfo__["web"],
    project_urls=__pkginfo__.get("project_urls", {}),
    classifiers=__pkginfo__["classifiers"],
    data_files=__pkginfo__.get("data_files", None),
    ext_modules=__pkginfo__.get("ext_modules", None),
    python_requires="~=3.6",
    setup_requires=[],
    tests_require=["pytest", "pytest-benchmark"],
    install_requires=__pkginfo__.get("install_requires", None),
    extras_require={
        ':sys_platform=="win32"': ["colorama"],
        "docs": doc_extra_requires,
    },
    entry_points={
        "console_scripts": [
            "pylint = pylint:run_pylint",
            "epylint = pylint:run_epylint",
            "pyreverse = pylint:run_pyreverse",
            "symilar = pylint:run_symilar",
        ]
    },
    packages=setuptools.find_packages(),
)

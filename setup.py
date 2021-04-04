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


def install():
    setuptools.setup(
        name="pylint",
        version=__pkginfo__["__version__"],
        license="GPL-2.0-or-later",
        description="python code static checker",
        long_description=long_description,
        author="Python Code Quality Authority",
        author_email="code-quality@python.org",
        url="https://github.com/PyCQA/pylint",
        project_urls={"What's New": "https://pylint.pycqa.org/en/latest/whatsnew/"},
        classifiers=[
            "Development Status :: 6 - Mature",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3 :: Only",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Debuggers",
            "Topic :: Software Development :: Quality Assurance",
            "Topic :: Software Development :: Testing",
        ],
        packages=setuptools.find_packages(),
        python_requires="~=3.6",
        setup_requires=[],
        tests_require=test_requires,
        install_requires=[
            "astroid>=2.5.2,<2.7",
            "isort>=4.2.5,<6",
            "mccabe>=0.6,<0.7",
            "toml>=0.7.1",
        ],
        extras_require={
            ':sys_platform=="win32"': ["colorama"],
            "docs": doc_extra_requires,
            "dev": dev_extra_requires,
        },
        entry_points={
            "console_scripts": [
                "pylint = pylint:run_pylint",
                "epylint = pylint:run_epylint",
                "pyreverse = pylint:run_pyreverse",
                "symilar = pylint:run_symilar",
            ]
        },
    )


if __name__ == "__main__":
    install()

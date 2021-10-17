import sys

from setuptools import setup


class PylintIncompatiblePythonError(Exception):
    def __init__(self, version_info: sys._version_info) -> None:
        super().__init__(
            "The last version compatible with Python <= 3.6.2 is pylint '2.9.3'. "
            f"You're using {'.'.join(map(str, version_info[:3]))}. "
            "Please install pylint 2.9.3 explicitly or upgrade your python interpreter "
            "to at least 3.6.2. Remember that Python 3.6 end life is December 2021. "
            "See https://github.com/PyCQA/pylint/issues/5065 for more detail."
        )


if sys.version_info < (3, 6, 2):
    raise PylintIncompatiblePythonError(sys.version_info)

setup()

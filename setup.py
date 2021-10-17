import sys

from setuptools import setup


class PylintIncompatiblePythonError(Exception):
    def __init__(self, major, minor, patch):
        super().__init__(
            f"The last version compatible with python <= 3.6.2 is pylint '2.9.3'."
            f"You're using {major}.{minor}.{patch}. "
            "Please install pylint 2.9.3 explicitly or upgrade your python interpreter "
            "to at least 3.6.2. Remember that python 3.6 end life is December 2021."
            "See https://github.com/PyCQA/pylint/issues/5065 for more detail."
        )


version = sys.version_info[:3]
if version < (3, 6, 2):
    raise PylintIncompatiblePythonError(*version)

setup()

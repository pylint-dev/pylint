"""Check that we do not crash with a recursion error

https://github.com/PyCQA/pylint/issues/3159
"""
# pylint: disable=missing-docstring
from setuptools import Command, find_packages, setup


class AnyCommand(Command):
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def run():
        print("Do anything")


setup(
    name="Thing",
    version="1.0",
    packages=find_packages(),
    cmdclass={"anycommand": AnyCommand},
)

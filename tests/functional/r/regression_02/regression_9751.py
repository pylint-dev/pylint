"""
pylint 3.2.4 regression
https://github.com/pylint-dev/pylint/issues/9751
"""

# pylint: disable=missing-function-docstring

from typing import Any

def repro() -> Any:
    return 5

def main():
    x = repro() + 5
    print(x)

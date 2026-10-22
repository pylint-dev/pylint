"""A module whose dunders come before the imports."""

__all__ = ["main"]
__version__ = "1.0.0"

import os
import sys


def main():
    print(os.getcwd(), file=sys.stderr)

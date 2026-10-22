"""A module whose dunders come after the imports."""

import os
import sys

__all__ = ["main"]  # [misplaced-module-dunder]
__version__ = "1.0.0"  # [misplaced-module-dunder]


def main():
    print(os.getcwd(), file=sys.stderr)

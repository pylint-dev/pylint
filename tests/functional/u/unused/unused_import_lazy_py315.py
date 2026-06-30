"""PEP 810 lazy imports (Python 3.15) interact normally with unused-import."""
lazy import os
lazy import sys  # [unused-import]
lazy from pathlib import Path
lazy from collections import OrderedDict  # [unused-import]


def use():
    """Use the lazily-imported names so they are not flagged as unused."""
    return os.getcwd(), Path

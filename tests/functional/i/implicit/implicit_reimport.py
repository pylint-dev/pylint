"""Tests for implicit-reimport."""

# pylint: disable=missing-module-docstring,unused-import,wrong-import-order
# pylint: disable=consider-using-from-import,import-outside-toplevel,redefined-outer-name

import logging  # [implicit-reimport]
import logging.config

import os.path
import os  # [implicit-reimport]

import json
import json.decoder as decoder

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pathlib
else:
    import pathlib._abc


def separate_scope() -> None:
    """Imports in a different scope do not make the module import redundant."""
    import logging.handlers

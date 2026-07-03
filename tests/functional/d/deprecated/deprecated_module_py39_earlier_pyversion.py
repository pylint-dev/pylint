"""Test deprecated modules from Python 3.9,
but use an earlier --py-version and ensure a warning is still emitted.
"""
# pylint: disable=unused-import, import-error

import binhex  # [deprecated-module]

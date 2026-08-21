"""Checks import order rule"""
# pylint: disable=unused-import,wrong-import-position,wrong-import-order,using-constant-test
# pylint: disable=import-error,reimported,invalid-name
import six
import logging.config
import os.path
from astroid import are_exclusive
import logging  # [ungrouped-imports]
import unused_import
try:
    import os  # [ungrouped-imports]
except ImportError:
    pass
from os import pardir
import scipy
from os import sep
from astroid import exceptions # [ungrouped-imports]
if True:
    import logging.handlers  # [ungrouped-imports]
from os.path import join  # [ungrouped-imports]
# Test related to compatibility with isort:
# We check that we do not create error with the old way pylint was handling it
import subprocess
import unittest
from unittest import TestCase
from unittest.mock import MagicMock


# https://github.com/pylint-dev/pylint/issues/3382
# Imports in a `if TYPE_CHECKING` block should not trigger `ungrouped-imports`
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import re
    from typing import List


# https://github.com/pylint-dev/pylint/issues/10460
# Imports in mutually exclusive OS guard branches (`os.name` / `sys.platform`)
# should not trigger `ungrouped-imports`
if os.name == "nt":
    from os import sep as nt_sep
    from os.path import abspath as nt_abspath
else:
    from os import pardir as nt_pardir
    from os.path import isabs as nt_isabs
import sys
if sys.platform == "win32":
    import re as win_re
else:
    import re as posix_re
from unittest import skip  # [ungrouped-imports]

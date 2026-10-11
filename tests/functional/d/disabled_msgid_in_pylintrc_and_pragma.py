"""A message disabled in the configuration must stay disabled on the lines
before a ``# pylint: disable`` pragma for the same message.

https://github.com/pylint-dev/pylint/issues/3945
"""

import os


def func():
    """A pragma that is not the first statement of the function."""
    import json
    # pylint: disable=unused-import
    import re


# pylint: disable=unused-import
import sys

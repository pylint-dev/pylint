"""Regression test for https://github.com/pylint-dev/pylint/issues/10043.

``importlib.abc.TraversableResources`` is deprecated since Python 3.12. An
import of it that only runs on older versions, behind a version guard, is
not a use of a deprecated class.
"""
# pylint: disable=unused-import

import sys

if sys.version_info >= (3, 12):
    from importlib.resources.abc import TraversableResources
else:
    from importlib.abc import TraversableResources

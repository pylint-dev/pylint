"""Test deprecated modules from Python 3.3."""
# pylint: disable=unused-import,import-error,no-name-in-module

from collections import Iterable  # [deprecated-class]

import collections.Set  # [deprecated-class]

import collections


_ = collections.Awaitable()  # [deprecated-class]

"""Test deprecated classes of modules that are listed for several Python versions.

The classes deprecated in an older version must still be reported when a newer
version adds more deprecated classes to the same module.
"""
# pylint: disable=unused-import,import-error,no-name-in-module,abstract-class-instantiated

import asyncio
import typing
from ast import Num  # [deprecated-class]
from importlib.abc import Finder  # [deprecated-class]
from typing import ByteString, Text  # [deprecated-class, deprecated-class]
from webbrowser import MacOSX  # [deprecated-class]

typing.Hashable()  # [deprecated-class]
asyncio.SafeChildWatcher()  # [deprecated-class]
asyncio.DefaultEventLoopPolicy()  # [deprecated-class]

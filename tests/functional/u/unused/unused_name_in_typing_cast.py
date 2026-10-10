"""Test if pylint sees names inside the string type argument of ``typing.cast``. #7548"""
# pylint: disable=invalid-name

import typing as t
from collections import OrderedDict
from decimal import Decimal  # [unused-import]
from fractions import Fraction
from ipaddress import IPv4Address
from pathlib import Path
from typing import Literal, cast
from uuid import UUID  # [unused-import]

# unused-import shouldn't be emitted for Path, OrderedDict, IPv4Address or Fraction
paths = t.cast("set[Path]", set())
ordered = cast("OrderedDict[str, int]", {})
addresses = cast(list["IPv4Address"], [])
fraction = cast(typ="Fraction", val=None)

# Strings outside of the type argument are not type annotations
decimal = cast(str, "Decimal")
uuid = cast(typ=Literal["UUID"], val="UUID")
print("Decimal", "UUID")
NAMES = ("Decimal", "UUID")


def local_type_alias(value):
    """unused-variable shouldn't be emitted for Alias."""
    Alias = int
    return cast("Alias", value)

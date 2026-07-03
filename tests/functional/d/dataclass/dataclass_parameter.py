"""Tests for dataclass and checks that check for parameters."""

import dataclasses
from dataclasses import KW_ONLY as keyword_only
from dataclasses import dataclass


@dataclass
class MyDataClass:
    """Simple dataclass with a KW_ONLY parameter."""

    _: dataclasses.KW_ONLY
    data: str


MyDataClass(data="test")


@dataclass
class MyDataClassWithAliases:
    """Simple dataclass with an aliased KW_ONLY parameter."""

    _: keyword_only
    data: str


MyDataClassWithAliases(data="test")

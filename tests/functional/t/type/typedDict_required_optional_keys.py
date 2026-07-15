"""Test TypedDict __required_keys__ and __optional_keys__ access."""
# pylint: disable=invalid-name,missing-class-docstring,pointless-statement,too-few-public-methods
from typing import TypedDict
from typing_extensions import TypedDict as TypedDictExt


class CustomTD(TypedDict):
    required: str
    optional: str


class CustomTDExt(TypedDictExt):
    required: str


class Child(CustomTD):
    extra: str


# Accessing __required_keys__ / __optional_keys__ on a TypedDict class is valid.
print(CustomTD.__required_keys__)
print(CustomTD.__optional_keys__)
print(CustomTDExt.__required_keys__)
print(Child.__required_keys__)

# Instances are regular dicts and do not have these attributes.
print(CustomTD().__required_keys__)  # [no-member]
print(CustomTD().__optional_keys__)  # [no-member]

# Regular classes do not have these attributes.
class Regular:
    pass

print(Regular.__required_keys__)  # [no-member]

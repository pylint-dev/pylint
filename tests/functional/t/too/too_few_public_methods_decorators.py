"""Classes decorated with ``attr`` or ``dataclasses`` decorators are exempt no
matter how the module that provides the decorator was imported (#3732).
"""
# pylint: disable=missing-docstring,import-error

import dataclasses as dc
from types import SimpleNamespace

import attr
from attr import s as attr_s

from .attr import s as relative_s


@attr.s
class AttrS:
    x: int


@attr.s(auto_attribs=True)
class AttrSCall:
    x: int


@attr.attrs
class AttrAttrs:
    x: int


@attr.attributes
class AttrAttributes:
    x: int


@attr.dataclass(frozen=True)
class AttrDataclass:
    ham: str
    spam: str


@attr.define
class AttrDefine:
    x: int


@attr.mutable
class AttrMutable:
    x: int


@attr.frozen
class AttrFrozen:
    x: int


@attr_s
class AttrAliasedDecorator:
    x: int


@dc.dataclass
class DataclassAliasedModule:
    x: int


def s(cls):
    return cls


def mutable(cls):
    return cls


HOLDER = SimpleNamespace(s=lambda cls: cls)


# Decorators that are only named like the attrs ones are not exempt.
@s
class UserDecoratorNamedS:  # [too-few-public-methods]
    x: int


@mutable
class UserDecoratorNamedMutable:  # [too-few-public-methods]
    x: int


# Only names bound by an import are followed, so a local object is not exempt.
@HOLDER.s
class DecoratorFromLocalObject:  # [too-few-public-methods]
    x: int


# A relative import names a local module, not attrs.
@relative_s
class DecoratorFromRelativeImport:  # [too-few-public-methods]
    x: int

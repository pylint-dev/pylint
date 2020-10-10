# pylint: disable=missing-docstring
import typing


class Hasher(typing.Protocol):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""

    def update(self, blob: bytes):
        ...

    def digest(self) -> bytes:
        ...


Generic = typing.TypeVar("Generic")


class HasherGeneric(typing.Protocol[Generic]):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""
    def update(self, blob: bytes):
        ...
    def digest(self) -> bytes:
        ...

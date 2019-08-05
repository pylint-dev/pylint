# pylint: disable=missing-docstring
import typing


class Hasher(typing.Protocol):
    """A hashing algorithm, e.g. :func:`hashlib.sha256`."""

    def update(self, blob: bytes):
        ...

    def digest(self) -> bytes:
        ...

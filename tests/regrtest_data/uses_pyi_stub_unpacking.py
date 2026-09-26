"""Unpack values returned by functions that are only declared in a stub."""
from pyi_stub_unpacking import declared_int, declared_tuple

FIRST, SECOND, THIRD = declared_tuple()
VALUE, _REST = declared_int()

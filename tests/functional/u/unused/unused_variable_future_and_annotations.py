"""Test `unused-variable` is not emitted for either case of `__future__.annotations` or `__all__`"""


from __future__ import annotations


__all__ = [ "apple" ]


def apple():
    """A public function"""

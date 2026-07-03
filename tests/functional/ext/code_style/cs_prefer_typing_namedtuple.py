# pylint: disable=missing-docstring
from collections import namedtuple

NoteHash = namedtuple('NoteHash', ['Pitch', 'Duration', 'Offset'])  # [prefer-typing-namedtuple]

class SearchMatch(
    namedtuple('SearchMatch', ['els', 'index', 'iterator'])  # [prefer-typing-namedtuple]
):
    """Adapted from primer package `music21`."""


# Regression test for https://github.com/pylint-dev/pylint/issues/10708
x = slice(42)
x()  # pylint: disable=not-callable

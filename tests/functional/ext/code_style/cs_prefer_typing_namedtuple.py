# pylint: disable=missing-docstring
from collections import namedtuple

NoteHash = namedtuple('NoteHash', ['Pitch', 'Duration', 'Offset'])  # [prefer-typing-namedtuple]

class SearchMatch(
    namedtuple('SearchMatch', ['els', 'index', 'iterator'])  # [prefer-typing-namedtuple]
):
    """Adapted from primer package `music21`."""

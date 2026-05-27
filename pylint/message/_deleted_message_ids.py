# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

from collections.abc import Sequence
from functools import cache
from typing import NamedTuple


class DeletedMessage(NamedTuple):
    msgid: str
    symbol: str
    old_names: Sequence[tuple[str, str]] = ()
    removed_in: str | None = None
    """First pylint release that no longer ships this message."""
    original_message: str | None = None
    """Short message text the symbol used to emit.

    Recovered from
    ``git show <removal-commit>~1:<source>`` for documentation use.
    """


class DeletedMessageData(NamedTuple):
    """A permanently removed message, used for documentation generation only.

    A flattened view of ``DeletedMessage``: each entry in this form represents
    either a canonical deleted symbol (``deleted_symbol=None``) or one of its
    pre-rename old names (``deleted_symbol`` pointing at the canonical one).
    """

    msgid: str
    symbol: str
    reason: str
    removed_in: str | None = None
    original_message: str | None = None
    deleted_symbol: str | None = None
    """If set, this entry is an old name of a deleted message; the value is the
    most recent symbol the message had before being deleted.
    """


DELETED_MSGID_PREFIXES: list[int] = []

# The ``removed_in`` field is the first release tag containing the removal commit
# (``git tag --contains <commit> | sort -V | head -1``). The ``original_message``
# field is the short message text the symbol last emitted, recovered from
# ``git show <removal-commit>~1:<source>``. Both fields are documentation-only.
DELETED_MESSAGES_IDS = {
    # Everything until the next comment is from the PY3K+ checker
    "https://github.com/pylint-dev/pylint/pull/4942": [
        DeletedMessage(
            "E1601",
            "print-statement",
            removed_in="2.11.0",
            original_message="print statement used",
        ),
        DeletedMessage(
            "E1602",
            "parameter-unpacking",
            removed_in="2.11.0",
            original_message="Parameter unpacking specified",
        ),
        DeletedMessage(
            "E1603",
            "unpacking-in-except",
            [("W0712", "old-unpacking-in-except")],
            removed_in="2.11.0",
            original_message=(
                "Implicit unpacking of exceptions is not supported in Python 3"
            ),
        ),
        DeletedMessage(
            "E1604",
            "old-raise-syntax",
            [("W0121", "old-old-raise-syntax")],
            removed_in="2.11.0",
            original_message=(
                "Use raise ErrorClass(args) instead of raise ErrorClass, args."
            ),
        ),
        DeletedMessage(
            "E1605",
            "backtick",
            [("W0333", "old-backtick")],
            removed_in="2.11.0",
            original_message="Use of the `` operator",
        ),
        DeletedMessage(
            "E1609",
            "import-star-module-level",
            removed_in="2.11.0",
            original_message="Import * only allowed at module level",
        ),
        DeletedMessage(
            "W1601",
            "apply-builtin",
            removed_in="2.11.0",
            original_message="apply built-in referenced",
        ),
        DeletedMessage(
            "W1602",
            "basestring-builtin",
            removed_in="2.11.0",
            original_message="basestring built-in referenced",
        ),
        DeletedMessage(
            "W1603",
            "buffer-builtin",
            removed_in="2.11.0",
            original_message="buffer built-in referenced",
        ),
        DeletedMessage(
            "W1604",
            "cmp-builtin",
            removed_in="2.11.0",
            original_message="cmp built-in referenced",
        ),
        DeletedMessage(
            "W1605",
            "coerce-builtin",
            removed_in="2.11.0",
            original_message="coerce built-in referenced",
        ),
        DeletedMessage(
            "W1606",
            "execfile-builtin",
            removed_in="2.11.0",
            original_message="execfile built-in referenced",
        ),
        DeletedMessage(
            "W1607",
            "file-builtin",
            removed_in="2.11.0",
            original_message="file built-in referenced",
        ),
        DeletedMessage(
            "W1608",
            "long-builtin",
            removed_in="2.11.0",
            original_message="long built-in referenced",
        ),
        DeletedMessage("W1609", "raw_input-builtin", removed_in="2.11.0"),
        DeletedMessage(
            "W1610",
            "reduce-builtin",
            removed_in="2.11.0",
            original_message="reduce built-in referenced",
        ),
        DeletedMessage(
            "W1611",
            "standarderror-builtin",
            removed_in="2.11.0",
            original_message="StandardError built-in referenced",
        ),
        DeletedMessage(
            "W1612",
            "unicode-builtin",
            removed_in="2.11.0",
            original_message="unicode built-in referenced",
        ),
        DeletedMessage(
            "W1613",
            "xrange-builtin",
            removed_in="2.11.0",
            original_message="xrange built-in referenced",
        ),
        DeletedMessage(
            "W1614",
            "coerce-method",
            removed_in="2.11.0",
            original_message="__coerce__ method defined",
        ),
        DeletedMessage(
            "W1615",
            "delslice-method",
            removed_in="2.11.0",
            original_message="__delslice__ method defined",
        ),
        DeletedMessage(
            "W1616",
            "getslice-method",
            removed_in="2.11.0",
            original_message="__getslice__ method defined",
        ),
        DeletedMessage(
            "W1617",
            "setslice-method",
            removed_in="2.11.0",
            original_message="__setslice__ method defined",
        ),
        DeletedMessage(
            "W1618",
            "no-absolute-import",
            removed_in="2.11.0",
            original_message="import missing `from __future__ import absolute_import`",
        ),
        DeletedMessage(
            "W1619",
            "old-division",
            removed_in="2.11.0",
            original_message="division w/o __future__ statement",
        ),
        DeletedMessage(
            "W1620",
            "dict-iter-method",
            removed_in="2.11.0",
            original_message="Calling a dict.iter*() method",
        ),
        DeletedMessage(
            "W1621",
            "dict-view-method",
            removed_in="2.11.0",
            original_message="Calling a dict.view*() method",
        ),
        DeletedMessage(
            "W1622",
            "next-method-called",
            removed_in="2.11.0",
            original_message="Called a next() method on an object",
        ),
        DeletedMessage(
            "W1623",
            "metaclass-assignment",
            removed_in="2.11.0",
            original_message="Assigning to a class's __metaclass__ attribute",
        ),
        DeletedMessage(
            "W1624",
            "indexing-exception",
            [("W0713", "old-indexing-exception")],
            removed_in="2.11.0",
            original_message="Indexing exceptions will not work on Python 3",
        ),
        DeletedMessage(
            "W1625",
            "raising-string",
            [("W0701", "old-raising-string")],
            removed_in="2.11.0",
            original_message="Raising a string exception",
        ),
        DeletedMessage(
            "W1626",
            "reload-builtin",
            removed_in="2.11.0",
            original_message="reload built-in referenced",
        ),
        DeletedMessage(
            "W1627",
            "oct-method",
            removed_in="2.11.0",
            original_message="__oct__ method defined",
        ),
        DeletedMessage(
            "W1628",
            "hex-method",
            removed_in="2.11.0",
            original_message="__hex__ method defined",
        ),
        DeletedMessage(
            "W1629",
            "nonzero-method",
            removed_in="2.11.0",
            original_message="__nonzero__ method defined",
        ),
        DeletedMessage(
            "W1630",
            "cmp-method",
            removed_in="2.11.0",
            original_message="__cmp__ method defined",
        ),
        DeletedMessage(
            "W1632",
            "input-builtin",
            removed_in="2.11.0",
            original_message="input built-in referenced",
        ),
        DeletedMessage(
            "W1633",
            "round-builtin",
            removed_in="2.11.0",
            original_message="round built-in referenced",
        ),
        DeletedMessage(
            "W1634",
            "intern-builtin",
            removed_in="2.11.0",
            original_message="intern built-in referenced",
        ),
        DeletedMessage(
            "W1635",
            "unichr-builtin",
            removed_in="2.11.0",
            original_message="unichr built-in referenced",
        ),
        DeletedMessage(
            "W1636",
            "map-builtin-not-iterating",
            [("W1631", "implicit-map-evaluation")],
            removed_in="2.11.0",
            original_message="map built-in referenced when not iterating",
        ),
        DeletedMessage(
            "W1637",
            "zip-builtin-not-iterating",
            removed_in="2.11.0",
            original_message="zip built-in referenced when not iterating",
        ),
        DeletedMessage(
            "W1638",
            "range-builtin-not-iterating",
            removed_in="2.11.0",
            original_message="range built-in referenced when not iterating",
        ),
        DeletedMessage(
            "W1639",
            "filter-builtin-not-iterating",
            removed_in="2.11.0",
            original_message="filter built-in referenced when not iterating",
        ),
        DeletedMessage(
            "W1640",
            "using-cmp-argument",
            removed_in="2.11.0",
            original_message="Using the cmp argument for list.sort / sorted",
        ),
        DeletedMessage(
            "W1642",
            "div-method",
            removed_in="2.11.0",
            original_message="__div__ method defined",
        ),
        DeletedMessage(
            "W1643",
            "idiv-method",
            removed_in="2.11.0",
            original_message="__idiv__ method defined",
        ),
        DeletedMessage(
            "W1644",
            "rdiv-method",
            removed_in="2.11.0",
            original_message="__rdiv__ method defined",
        ),
        DeletedMessage(
            "W1645",
            "exception-message-attribute",
            removed_in="2.11.0",
            original_message="Exception.message removed in Python 3",
        ),
        DeletedMessage(
            "W1646",
            "invalid-str-codec",
            removed_in="2.11.0",
            original_message="non-text encoding used in str.decode",
        ),
        DeletedMessage(
            "W1647",
            "sys-max-int",
            removed_in="2.11.0",
            original_message="sys.maxint removed in Python 3",
        ),
        DeletedMessage(
            "W1648",
            "bad-python3-import",
            removed_in="2.11.0",
            original_message="Module moved in Python 3",
        ),
        DeletedMessage(
            "W1649",
            "deprecated-string-function",
            removed_in="2.11.0",
            original_message="Accessing a deprecated function on the string module",
        ),
        DeletedMessage(
            "W1650",
            "deprecated-str-translate-call",
            removed_in="2.11.0",
            original_message=(
                "Using str.translate with deprecated deletechars parameters"
            ),
        ),
        DeletedMessage(
            "W1651",
            "deprecated-itertools-function",
            removed_in="2.11.0",
            original_message="Accessing a deprecated function on the itertools module",
        ),
        DeletedMessage(
            "W1652",
            "deprecated-types-field",
            removed_in="2.11.0",
            original_message="Accessing a deprecated fields on the types module",
        ),
        DeletedMessage(
            "W1653",
            "next-method-defined",
            removed_in="2.11.0",
            original_message="next method defined",
        ),
        DeletedMessage(
            "W1654",
            "dict-items-not-iterating",
            removed_in="2.11.0",
            original_message="dict.items referenced when not iterating",
        ),
        DeletedMessage(
            "W1655",
            "dict-keys-not-iterating",
            removed_in="2.11.0",
            original_message="dict.keys referenced when not iterating",
        ),
        DeletedMessage(
            "W1656",
            "dict-values-not-iterating",
            removed_in="2.11.0",
            original_message="dict.values referenced when not iterating",
        ),
        DeletedMessage(
            "W1657",
            "deprecated-operator-function",
            removed_in="2.11.0",
            original_message="Accessing a removed attribute on the operator module",
        ),
        DeletedMessage(
            "W1658",
            "deprecated-urllib-function",
            removed_in="2.11.0",
            original_message="Accessing a removed attribute on the urllib module",
        ),
        DeletedMessage(
            "W1659",
            "xreadlines-attribute",
            removed_in="2.11.0",
            original_message="Accessing a removed xreadlines attribute",
        ),
        DeletedMessage(
            "W1660",
            "deprecated-sys-function",
            removed_in="2.11.0",
            original_message="Accessing a removed attribute on the sys module",
        ),
        DeletedMessage(
            "W1661",
            "exception-escape",
            removed_in="2.11.0",
            original_message=(
                "Using an exception object that was bound by an except handler"
            ),
        ),
        DeletedMessage(
            "W1662",
            "comprehension-escape",
            removed_in="2.11.0",
            original_message="Using a variable that was bound inside a comprehension",
        ),
    ],
    "https://github.com/pylint-dev/pylint/pull/3578": [
        DeletedMessage(
            "W0312",
            "mixed-indentation",
            removed_in="2.6.0",
            original_message="Found indentation with %ss instead of %ss",
        ),
    ],
    "https://github.com/pylint-dev/pylint/pull/3577": [
        DeletedMessage(
            "C0326",
            "bad-whitespace",
            [
                ("C0323", "no-space-after-operator"),
                ("C0324", "no-space-after-comma"),
                ("C0322", "no-space-before-operator"),
            ],
            removed_in="2.6.0",
            original_message="%s space %s %s %s\n%s",
        ),
    ],
    "https://github.com/pylint-dev/pylint/pull/3571": [
        DeletedMessage(
            "C0330",
            "bad-continuation",
            removed_in="2.6.0",
            original_message="Wrong %s indentation%s%s.\n%s%s",
        ),
    ],
    "https://pylint.readthedocs.io/en/latest/whatsnew/1/1.4.html#what-s-new-in-pylint-1-4-3": [
        DeletedMessage(
            "R0921",
            "abstract-class-not-used",
            removed_in="1.4.3",
            original_message="Abstract class not referenced",
        ),
        DeletedMessage(
            "R0922",
            "abstract-class-little-used",
            removed_in="1.4.3",
            original_message="Abstract class is only referenced %s times",
        ),
        DeletedMessage(
            "W0142",
            "star-args",
            removed_in="1.4.3",
            original_message="Used * or ** magic",
        ),
    ],
    "https://github.com/pylint-dev/pylint/issues/2409": [
        DeletedMessage(
            "W0232",
            "no-init",
            removed_in="2.14.0",
            original_message="Class has no __init__ method",
        ),
    ],
    "https://github.com/pylint-dev/pylint/pull/6421": [
        DeletedMessage(
            "W0111",
            "assign-to-new-keyword",
            removed_in="2.14.0",
            original_message="Name %s will become a keyword in Python %s",
        ),
    ],
}
MOVED_TO_EXTENSIONS = {
    "https://pylint.readthedocs.io/en/latest/whatsnew/2/2.14/summary.html#removed-checkers": [
        DeletedMessage("R0201", "no-self-use")
    ],
}


@cache
def is_deleted_symbol(symbol: str) -> str | None:
    """Return the explanation for removal if the message was removed."""
    for explanation, deleted_messages in DELETED_MESSAGES_IDS.items():
        for deleted_message in deleted_messages:
            if symbol == deleted_message.symbol or any(
                symbol == m[1] for m in deleted_message.old_names
            ):
                return explanation
    return None


@cache
def is_deleted_msgid(msgid: str) -> str | None:
    """Return the explanation for removal if the message was removed."""
    for explanation, deleted_messages in DELETED_MESSAGES_IDS.items():
        for deleted_message in deleted_messages:
            if msgid == deleted_message.msgid or any(
                msgid == m[0] for m in deleted_message.old_names
            ):
                return explanation
    return None


@cache
def is_moved_symbol(symbol: str) -> str | None:
    """Return the explanation for moving if the message was moved to extensions."""
    for explanation, moved_messages in MOVED_TO_EXTENSIONS.items():
        for moved_message in moved_messages:
            if symbol == moved_message.symbol or any(
                symbol == m[1] for m in moved_message.old_names
            ):
                return explanation
    return None


@cache
def is_moved_msgid(msgid: str) -> str | None:
    """Return the explanation for moving if the message was moved to extensions."""
    for explanation, moved_messages in MOVED_TO_EXTENSIONS.items():
        for moved_message in moved_messages:
            if msgid == moved_message.msgid or any(
                msgid == m[0] for m in moved_message.old_names
            ):
                return explanation
    return None

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

from __future__ import annotations

try:
    import isort.api
    import isort.settings

    HAS_ISORT_5 = True
except ImportError:  # isort < 5
    import isort

    HAS_ISORT_5 = False

import argparse
import codecs
import os
import sys
import textwrap
import tokenize
from collections.abc import Sequence
from io import BufferedReader, BytesIO
from typing import TYPE_CHECKING, List, Pattern, Tuple, TypeVar, Union

from astroid import Module, modutils, nodes

from pylint.constants import PY_EXTS

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

if TYPE_CHECKING:
    from pylint.lint import PyLinter

DEFAULT_LINE_LENGTH = 79

# These are types used to overload get_global_option() and refer to the options type
GLOBAL_OPTION_BOOL = Literal[
    "suggestion-mode",
    "analyse-fallback-blocks",
    "allow-global-unused-variables",
]
GLOBAL_OPTION_INT = Literal["max-line-length", "docstring-min-length"]
GLOBAL_OPTION_LIST = Literal["ignored-modules"]
GLOBAL_OPTION_PATTERN = Literal[
    "no-docstring-rgx",
    "dummy-variables-rgx",
    "ignored-argument-names",
    "mixin-class-rgx",
]
GLOBAL_OPTION_PATTERN_LIST = Literal["exclude-too-few-public-methods", "ignore-paths"]
GLOBAL_OPTION_TUPLE_INT = Literal["py-version"]
GLOBAL_OPTION_NAMES = Union[
    GLOBAL_OPTION_BOOL,
    GLOBAL_OPTION_INT,
    GLOBAL_OPTION_LIST,
    GLOBAL_OPTION_PATTERN,
    GLOBAL_OPTION_PATTERN_LIST,
    GLOBAL_OPTION_TUPLE_INT,
]
T_GlobalOptionReturnTypes = TypeVar(
    "T_GlobalOptionReturnTypes",
    bool,
    int,
    List[str],
    Pattern[str],
    List[Pattern[str]],
    Tuple[int, ...],
)


def normalize_text(
    text: str, line_len: int = DEFAULT_LINE_LENGTH, indent: str = ""
) -> str:
    """Wrap the text on the given line length."""
    return "\n".join(
        textwrap.wrap(
            text, width=line_len, initial_indent=indent, subsequent_indent=indent
        )
    )


CMPS = ["=", "-", "+"]


# py3k has no more cmp builtin
def cmp(a: int | float, b: int | float) -> int:
    return (a > b) - (a < b)


def diff_string(old: int | float, new: int | float) -> str:
    """Given an old and new int value, return a string representing the
    difference.
    """
    diff = abs(old - new)
    diff_str = f"{CMPS[cmp(old, new)]}{diff and f'{diff:.2f}' or ''}"
    return diff_str


def get_module_and_frameid(node: nodes.NodeNG) -> tuple[str, str]:
    """Return the module name and the frame id in the module."""
    frame = node.frame(future=True)
    module, obj = "", []
    while frame:
        if isinstance(frame, Module):
            module = frame.name
        else:
            obj.append(getattr(frame, "name", "<lambda>"))
        try:
            frame = frame.parent.frame(future=True)
        except AttributeError:
            break
    obj.reverse()
    return module, ".".join(obj)


def get_rst_title(title: str, character: str) -> str:
    """Permit to get a title formatted as ReStructuredText test (underlined with a
    chosen character).
    """
    return f"{title}\n{character * len(title)}\n"


def decoding_stream(
    stream: BufferedReader | BytesIO,
    encoding: str,
    errors: Literal["strict"] = "strict",
) -> codecs.StreamReader:
    try:
        reader_cls = codecs.getreader(encoding or sys.getdefaultencoding())
    except LookupError:
        reader_cls = codecs.getreader(sys.getdefaultencoding())
    return reader_cls(stream, errors)


def tokenize_module(node: nodes.Module) -> list[tokenize.TokenInfo]:
    with node.stream() as stream:
        readline = stream.readline
        return list(tokenize.tokenize(readline))


def register_plugins(linter: PyLinter, directory: str) -> None:
    """Load all module and package in the given directory, looking for a
    'register' function in each one, used to register pylint checkers.
    """
    imported = {}
    for filename in os.listdir(directory):
        base, extension = os.path.splitext(filename)
        if base in imported or base == "__pycache__":
            continue
        if (
            extension in PY_EXTS
            and base != "__init__"
            or (
                not extension
                and os.path.isdir(os.path.join(directory, base))
                and not filename.startswith(".")
            )
        ):
            try:
                module = modutils.load_module_from_file(
                    os.path.join(directory, filename)
                )
            except ValueError:
                # empty module name (usually Emacs auto-save files)
                continue
            except ImportError as exc:
                print(f"Problem importing module {filename}: {exc}", file=sys.stderr)
            else:
                if hasattr(module, "register"):
                    module.register(linter)
                    imported[base] = 1


def _splitstrip(string: str, sep: str = ",") -> list[str]:
    """Return a list of stripped string by splitting the string given as
    argument on `sep` (',' by default), empty strings are discarded.

    >>> _splitstrip('a, b, c   ,  4,,')
    ['a', 'b', 'c', '4']
    >>> _splitstrip('a')
    ['a']
    >>> _splitstrip('a,\nb,\nc,')
    ['a', 'b', 'c']

    :type string: str or unicode
    :param string: a csv line

    :type sep: str or unicode
    :param sep: field separator, default to the comma (',')

    :rtype: str or unicode
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    return [word.strip() for word in string.split(sep) if word.strip()]


def _unquote(string: str) -> str:
    """Remove optional quotes (simple or double) from the string.

    :param string: an optionally quoted string
    :return: the unquoted string (or the input string if it wasn't quoted)
    """
    if not string:
        return string
    if string[0] in "\"'":
        string = string[1:]
    if string[-1] in "\"'":
        string = string[:-1]
    return string


def _check_csv(value: list[str] | tuple[str] | str) -> Sequence[str]:
    if isinstance(value, (list, tuple)):
        return value
    return _splitstrip(value)


def _comment(string: str) -> str:
    """Return string as a comment."""
    lines = [line.strip() for line in string.splitlines()]
    sep = "\n"
    return "# " + f"{sep}# ".join(lines)


class IsortDriver:
    """A wrapper around isort API that changed between versions 4 and 5."""

    def __init__(self, config: argparse.Namespace) -> None:
        if HAS_ISORT_5:
            self.isort5_config = isort.settings.Config(
                # There is no typo here. EXTRA_standard_library is
                # what most users want. The option has been named
                # KNOWN_standard_library for ages in pylint, and we
                # don't want to break compatibility.
                extra_standard_library=config.known_standard_library,
                known_third_party=config.known_third_party,
            )
        else:
            # pylint: disable-next=no-member
            self.isort4_obj = isort.SortImports(  # type: ignore[attr-defined]
                file_contents="",
                known_standard_library=config.known_standard_library,
                known_third_party=config.known_third_party,
            )

    def place_module(self, package: str) -> str:
        if HAS_ISORT_5:
            return isort.api.place_module(package, self.isort5_config)
        return self.isort4_obj.place_module(package)  # type: ignore[no-any-return]

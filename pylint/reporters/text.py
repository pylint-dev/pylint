# Copyright (c) 2006-2007, 2010-2014 LOGILAB S.A. (Paris, FRANCE) <contact@logilab.fr>
# Copyright (c) 2012-2014 Google, Inc.
# Copyright (c) 2014 Brett Cannon <brett@python.org>
# Copyright (c) 2014 Arun Persaud <arun@nubati.net>
# Copyright (c) 2015-2018, 2020 Claudiu Popa <pcmanticore@gmail.com>
# Copyright (c) 2015 Florian Bruhin <me@the-compiler.org>
# Copyright (c) 2015 Ionel Cristian Maries <contact@ionelmc.ro>
# Copyright (c) 2016 y2kbugger <y2kbugger@users.noreply.github.com>
# Copyright (c) 2018-2019 Nick Drozd <nicholasdrozd@gmail.com>
# Copyright (c) 2018 Sushobhit <31987769+sushobhit27@users.noreply.github.com>
# Copyright (c) 2018 Jace Browning <jacebrowning@gmail.com>
# Copyright (c) 2019-2021 Pierre Sassoulas <pierre.sassoulas@gmail.com>
# Copyright (c) 2019 Hugo van Kemenade <hugovk@users.noreply.github.com>
# Copyright (c) 2020 hippo91 <guillaume.peillex@gmail.com>
# Copyright (c) 2021 Daniël van Noord <13665637+DanielNoord@users.noreply.github.com>
# Copyright (c) 2021 Marc Mueller <30130371+cdce8p@users.noreply.github.com>

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE

"""Plain text reporters:

:text: the default one grouping messages by module
:colorized: an ANSI colorized text reporter
"""
import os
import sys
import warnings
from typing import TYPE_CHECKING, Dict, NamedTuple, Optional, Set, TextIO, Tuple

from pylint.interfaces import IReporter
from pylint.message import Message
from pylint.reporters import BaseReporter
from pylint.reporters.ureports.text_writer import TextWriter

if TYPE_CHECKING:
    from pylint.lint import PyLinter
    from pylint.reporters.ureports.nodes import Section


class MessageStyle(NamedTuple):
    """Styling of a message"""

    colour: Optional[str]
    """The colour name (see `ANSI_COLORS` for available values)
    or the colour number when 256 colors are available
    """
    style: Tuple[str, ...]
    """Tuple of style strings (see `ANSI_COLORS` for available values).
    """


ColorMappingDict = Dict[str, MessageStyle]

TITLE_UNDERLINES = ["", "=", "-", "."]

ANSI_PREFIX = "\033["
ANSI_END = "m"
ANSI_RESET = "\033[0m"
ANSI_STYLES = {
    "reset": "0",
    "bold": "1",
    "italic": "3",
    "underline": "4",
    "blink": "5",
    "inverse": "7",
    "strike": "9",
}
ANSI_COLORS = {
    "reset": "0",
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
}


def _get_ansi_code(msg_style: MessageStyle) -> str:
    """return ansi escape code corresponding to color and style

    :param msg_style: the message style

    :raise KeyError: if an unexistent color or style identifier is given

    :return: the built escape code
    """
    ansi_code = []
    if msg_style.style == ():
        for effect in msg_style.style:
            ansi_code.append(ANSI_STYLES[effect])
    if msg_style.colour:
        if msg_style.colour.isdigit():
            ansi_code.extend(["38", "5"])
            ansi_code.append(msg_style.colour)
        else:
            ansi_code.append(ANSI_COLORS[msg_style.colour])
    if ansi_code:
        return ANSI_PREFIX + ";".join(ansi_code) + ANSI_END
    return ""


def colorize_ansi(msg: str, msg_style: MessageStyle) -> str:
    """colorize message by wrapping it with ansi escape codes

    :param msg: the message string to colorize


    :param msg_style: the message style

    :raise KeyError: if an unexistent color or style identifier is given

    :return: the ansi escaped string
    """
    # If both color and style are not defined, then leave the text as is
    if msg_style.colour is None and msg_style.style == ():
        return msg
    escape_code = _get_ansi_code(msg_style)
    # If invalid (or unknown) color, don't wrap msg with ansi codes
    if escape_code:
        return f"{escape_code}{msg}{ANSI_RESET}"
    return msg


class TextReporter(BaseReporter):
    """Reports messages and layouts in plain text"""

    __implements__ = IReporter
    name = "text"
    extension = "txt"
    line_format = "{path}:{line}:{column}: {msg_id}: {msg} ({symbol})"

    def __init__(self, output: Optional[TextIO] = None) -> None:
        BaseReporter.__init__(self, output)
        self._modules: Set[str] = set()
        self._template = self.line_format

    def on_set_current_module(self, module: str, filepath: Optional[str]) -> None:
        self._template = str(self.linter.config.msg_template or self._template)

    def write_message(self, msg: Message) -> None:
        """Convenience method to write a formatted message with class default template"""
        self.writeln(msg.format(self._template))

    def handle_message(self, msg: Message) -> None:
        """manage message of different type and in the context of path"""
        if msg.module not in self._modules:
            if msg.module:
                self.writeln(f"************* Module {msg.module}")
                self._modules.add(msg.module)
            else:
                self.writeln("************* ")
        self.write_message(msg)

    def _display(self, layout: "Section") -> None:
        """launch layouts display"""
        print(file=self.out)
        TextWriter().format(layout, self.out)


class ParseableTextReporter(TextReporter):
    """a reporter very similar to TextReporter, but display messages in a form
    recognized by most text editors :

    <filename>:<linenum>:<msg>
    """

    name = "parseable"
    line_format = "{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}"

    def __init__(self, output: Optional[TextIO] = None) -> None:
        warnings.warn(
            f"{self.name} output format is deprecated. This is equivalent to --msg-template={self.line_format}",
            DeprecationWarning,
        )
        TextReporter.__init__(self, output)


class VSTextReporter(ParseableTextReporter):
    """Visual studio text reporter"""

    name = "msvs"
    line_format = "{path}({line}): [{msg_id}({symbol}){obj}] {msg}"


class ColorizedTextReporter(TextReporter):
    """Simple TextReporter that colorizes text output"""

    name = "colorized"
    COLOR_MAPPING: ColorMappingDict = {
        "I": MessageStyle("green", ()),
        "C": MessageStyle(None, ("bold",)),
        "R": MessageStyle("magenta", ("bold", "italic")),
        "W": MessageStyle("magenta", ()),
        "E": MessageStyle("red", ("bold",)),
        "F": MessageStyle("red", ("bold", "underline")),
        "S": MessageStyle("yellow", ("inverse",)),  # S stands for module Separator
    }

    def __init__(
        self,
        output: Optional[TextIO] = None,
        color_mapping: Optional[ColorMappingDict] = None,
    ) -> None:
        TextReporter.__init__(self, output)
        self.color_mapping = color_mapping or dict(ColorizedTextReporter.COLOR_MAPPING)
        ansi_terms = ["xterm-16color", "xterm-256color"]
        if os.environ.get("TERM") not in ansi_terms:
            if sys.platform == "win32":
                # pylint: disable=import-error,import-outside-toplevel
                import colorama

                self.out = colorama.AnsiToWin32(self.out)

    def _get_decoration(self, msg_id: str) -> MessageStyle:
        """Returns the message style as defined in self.color_mapping"""
        try:
            return self.color_mapping[msg_id[0]]
        except KeyError:
            return MessageStyle(None, ())

    def handle_message(self, msg: Message) -> None:
        """manage message of different types, and colorize output
        using ansi escape codes
        """
        if msg.module not in self._modules:
            msg_style = self._get_decoration("S")
            if msg.module:
                modsep = colorize_ansi(f"************* Module {msg.module}", msg_style)
            else:
                modsep = colorize_ansi(f"************* {msg.module}", msg_style)
            self.writeln(modsep)
            self._modules.add(msg.module)
        msg_style = self._get_decoration(msg.C)

        msg = msg._replace(
            **{
                attr: colorize_ansi(getattr(msg, attr), msg_style)
                for attr in ("msg", "symbol", "category", "C")
            }
        )
        self.write_message(msg)


def register(linter: "PyLinter") -> None:
    """Register the reporter classes with the linter."""
    linter.register_reporter(TextReporter)
    linter.register_reporter(ParseableTextReporter)
    linter.register_reporter(VSTextReporter)
    linter.register_reporter(ColorizedTextReporter)

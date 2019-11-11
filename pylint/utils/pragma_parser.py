# -*- coding: utf-8 -*-

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

import re
from collections import namedtuple
from typing import Generator, List

# Allow stopping after the first semicolon/hash encountered,
# so that an option can be continued with the reasons
# why it is active or disabled.
OPTION_RGX = r"""
    \s*                # Any number of whithespace
    \#?                # One or zero hash
    .*                 # Anything (as much as possible)
    (\s*               # Beginning of first matched group and any number of whitespaces
    \#                 # Beginning of comment
    .*?                # Anything (as little as possible)
    \bpylint:          # pylint word and column
    \s*                # Any number of whitespaces
    ([^;#\n]+))        # Anything except semicolon or hash or newline (it is the second matched group) 
                       # and end of the first matched group
    [;#]{0,1}"""  # From 0 to 1 repetition of semicolon or hash
OPTION_PO = re.compile(OPTION_RGX, re.VERBOSE)


PragmaRepresenter = namedtuple("PragmaRepresenter", "action messages")


ATOMIC_KEYWORDS = ("disable-all", "skip-file")
MESSAGE_KEYWORDS = ("disable-msg", "enable-msg", "disable", "enable")
ALL_KEYWORDS = "|".join(ATOMIC_KEYWORDS + MESSAGE_KEYWORDS)


TOKEN_SPECIFICATION = [
    ("KEYWORD", r"\b({:s})\b".format(ALL_KEYWORDS)),
    ("MESSAGE_STRING", r"[A-Za-z\-]{2,}"),  #  Identifiers
    ("ASSIGN", r"="),  #  Assignment operator
    ("MESSAGE_NUMBER", r"[CREIWF]{1}\d*"),
]

TOK_REGEX = "|".join(
    "(?P<{:s}>{:s})".format(token_name, token_rgx)
    for token_name, token_rgx in TOKEN_SPECIFICATION
)


def emit_pragma_representer(action, messages):
    if not messages and action in MESSAGE_KEYWORDS:
        raise MissingMessage(
            "The keyword is not followed by message identifier", action
        )
    return PragmaRepresenter(action, messages)


class PragmaParserError(Exception):
    """
    A class for exceptions thrown by pragma_parser module
    """

    def __init__(self, message, token):
        """
        :args message: explain the reason why the exception has been thrown
        :args token: token concerned by the exception
        """
        self.message = message
        self.token = token
        super(PragmaParserError, self).__init__(self.message)


class UnknownKeyword(PragmaParserError):
    """
    Thrown in case the keyword is not recognized
    """


class MissingAssignment(PragmaParserError):
    """
    Thrown in case the = sign is missing
    """


class UnsupportedAssignment(PragmaParserError):
    """
    Throw in case the assignment sign follows a licit keyword but
    that doesn't support assignment
    """


class MissingKeyword(PragmaParserError):
    """
    Thrown in case keyword is missing
    """


class MissingMessage(PragmaParserError):
    """
    Thrown in case message identifier is missing
    """


def parse_pragma(pylint_pragma: str) -> Generator[PragmaRepresenter, None, None]:
    action = None
    messages = []  # type: List[str]
    assignment_required = False
    previous_token = ""

    for mo in re.finditer(TOK_REGEX, pylint_pragma):
        kind = mo.lastgroup
        value = mo.group()

        if kind == "ASSIGN":
            if not assignment_required:
                if action:
                    # A keyword has been found previously but doesn't support assignement
                    raise UnsupportedAssignment(
                        "The keyword doesn't support assignment", action
                    )
                if previous_token:
                    #  Something found previously but not a known keyword
                    raise UnknownKeyword("The keyword is not licit", previous_token)
                # Nothing at all detected before this assignment
                raise MissingKeyword("Missing keyword before assignment", "")
            assignment_required = False
        elif assignment_required:
            raise MissingAssignment("The = sign is missing after the keyword", action)
        elif kind == "KEYWORD":
            if action:
                yield emit_pragma_representer(action, messages)
            action = value
            messages = list()
            assignment_required = action in MESSAGE_KEYWORDS
        elif kind in ("MESSAGE_STRING", "MESSAGE_NUMBER"):
            messages.append(value)
            assignment_required = False
        else:
            raise RuntimeError("Token not recognized")

        previous_token = value

    if action:
        yield emit_pragma_representer(action, messages)
    else:
        raise UnknownKeyword("The keyword is not licit", previous_token)

"""Testing inconsistent returns involving typing.NoReturn annotations."""
# pylint: disable=missing-docstring, invalid-name

import sys
import typing

def parser_error(msg) -> typing.NoReturn:  # pylint: disable=unused-argument
    sys.exit(1)

def parser_error_nortype(msg):  # pylint: disable=unused-argument
    sys.exit(2)


from typing import NoReturn  # pylint: disable=wrong-import-position

def parser_error_name(msg) -> NoReturn:  # pylint: disable=unused-argument
    sys.exit(3)

def bug_pylint_4122(s):
    """
    Every returns is consistent because parser_error has type hints
    indicating it never returns
    """
    try:
        n = int(s)
        if n < 1:
            raise ValueError()
        return n
    except ValueError:
        parser_error('parser error')

def bug_pylint_4122_wrong(s):  # [inconsistent-return-statements]
    """
    Every returns is not consistent because parser_error_nortype has no type hints
    """
    try:
        n = int(s)
        if n < 1:
            raise ValueError()
        return n
    except ValueError:
        parser_error_nortype('parser error')

def bug_pylint_4122_bis(s):
    """
    Every returns is consistent because parser_error has type hints
    indicating it never returns
    """
    try:
        n = int(s)
        if n < 1:
            raise ValueError()
        return n
    except ValueError:
        parser_error_name('parser error')

"""Testing inconsistent returns involving typing.NoReturn annotations."""
# pylint: disable=missing-docstring, invalid-name

import sys
import typing

from pylint.constants import PY311_PLUS

if PY311_PLUS:
    from typing import assert_never  # pylint: disable=no-name-in-module
else:
    from typing_extensions import assert_never


def parser_error(msg) -> typing.NoReturn:  # pylint: disable=unused-argument
    sys.exit(1)

def parser_error_nortype(msg):  # pylint: disable=unused-argument
    sys.exit(2)


from typing import NoReturn  # pylint: disable=wrong-import-position,wrong-import-order

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

class ClassUnderTest:
    def _no_return_method(self) -> typing.NoReturn:
        sys.exit(1)

    def _falsely_no_return_method(self) -> typing.NoReturn:
        return 1

    def _does_return_method(self) -> int:
        return 1

    def bug_pylint_8747(self, s: str) -> int:
        """Every return is consistent because self._no_return_method hints NoReturn"""
        try:
            n = int(s)
            if n < 1:
                raise ValueError
            return n
        except ValueError:
            self._no_return_method()

    def bug_pylint_8747_wrong(self, s: str) -> int:  # [inconsistent-return-statements]
        """Every return is not consistent because self._does_return_method() returns a value"""
        try:
            n = int(s)
            if n < 1:
                raise ValueError
            return n
        except ValueError:
            self._does_return_method()

    def bug_pylint_8747_incorrect_annotation(self, s: str) -> int:
        """Every return is consistent since pylint does not attempt to detect that the
        NoReturn annotation is incorrect and the function actually returns
        """
        try:
            n = int(s)
            if n < 1:
                raise ValueError
            return n
        except ValueError:
            self._falsely_no_return_method()

# https://github.com/pylint-dev/pylint/issues/7565
def never_is_handled_like_noreturn(arg: typing.Union[int, str]) -> int:
    if isinstance(arg, int):
        return 1
    if isinstance(arg, str):
        return 2
    assert_never(arg)


def declared_to_not_return() -> None:
    return


def config_takes_precedence_over_inference(arg: typing.Union[int, str]) -> int:
    if isinstance(arg, int):
        return 1
    if isinstance(arg, str):
        return 2
    declared_to_not_return()


def unrelated() -> None:
    return


# +1: [inconsistent-return-statements]
def ensure_message(arg: typing.Union[int, str]) -> int:
    if isinstance(arg, int):
        return 1
    unrelated()

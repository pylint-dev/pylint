# pylint: disable=missing-function-docstring, missing-module-docstring, invalid-name, import-outside-toplevel
# pylint: disable=missing-class-docstring, too-few-public-methods, unused-variable, multiple-statements, line-too-long
# pylint: disable=contextmanager-generator-missing-cleanup
"""
Previously, open was uninferable on PyPy so we moved all functional tests
to a separate file. This is no longer the case but the files remain split.
"""
from contextlib import contextmanager
from pathlib import Path

myfile = open("test.txt", encoding="utf-8")  # [consider-using-with]


def test_open():
    fh = open("test.txt", encoding="utf-8")  # [consider-using-with]
    fh.close()

    with open("test.txt", encoding="utf-8") as fh:  # must not trigger
        fh.read()


def test_open_in_enter():
    """Message must not trigger if the resource is allocated in a context manager."""

    class MyContextManager:
        def __init__(self):
            self.file_handle = None

        def __enter__(self):
            self.file_handle = open("foo.txt", "w", encoding="utf-8")  # must not trigger

        def __exit__(self, exc_type, exc_value, traceback):
            self.file_handle.close()


@contextmanager
def test_open_in_with_contextlib():
    """Message must not trigger if the resource is allocated in a context manager."""
    file_handle = open("foo.txt", "w", encoding="utf-8")  # must not trigger
    yield file_handle
    file_handle.close()


def test_open_outside_assignment():
    open("foo", encoding="utf-8").read()  # [consider-using-with]
    content = open("foo", encoding="utf-8").read()  # [consider-using-with]


def test_open_inside_with_block():
    with open("foo", encoding="utf-8") as fh:
        open("bar", encoding="utf-8")  # [consider-using-with]


def test_ternary_if_in_with_block(file1, file2, which):
    """Regression test for issue #4676 (false positive)"""
    with (open(file1, encoding="utf-8") if which else open(file2, encoding="utf-8")) as input_file:  # must not trigger
        return input_file.read()


def test_single_line_with(file1):
    with open(file1, encoding="utf-8"): return file1.read()  # must not trigger


def test_multiline_with_items(file1, file2, which):
    with (open(file1, encoding="utf-8") if which
        else open(file2, encoding="utf-8")) as input_file: return input_file.read()


def test_suppress_on_return():
    return open("foo", encoding="utf8")  # must not trigger


class TestControlFlow:
    """
    The message is triggered if a context manager is assigned to a variable, which name is later
    reassigned without the variable being used inside a ``with`` first.
    E.g. the following would trigger the message:

        a = open("foo")  # <-- would trigger here
        a = "something new"

    But it must not happen that the logic which checks if the same variable is assigned multiple
    times in different code branches where only one of those assign statements is hit at runtime.
    For example, the variable could be assigned in an if-else construct.

    These tests check that the message is not triggered in those circumstances.
    """

    def test_defined_in_if_and_else(self, predicate):
        if predicate:
            file_handle = open("foo", encoding="utf8")  # must not trigger
        else:
            file_handle = open("bar", encoding="utf8")  # must not trigger
        with file_handle:
            return file_handle.read()

    def test_defined_in_else_only(self, predicate):
        if predicate:
            result = "shiny watermelon"
        else:
            file_handle = open("foo", encoding="utf8")  # must not trigger
            with file_handle:
                result = file_handle.read()
        return result

    def test_defined_in_if_only(self, predicate):
        if predicate:
            file_handle = open("foo", encoding="utf8")  # must not trigger
            with file_handle:
                result = file_handle.read()
        else:
            result = "shiny watermelon"
        return result

    def test_triggers_if_reassigned_after_if_else(self, predicate):
        if predicate:
            file_handle = open("foo", encoding="utf8")
        else:
            file_handle = open(  # [consider-using-with]
                "bar", encoding="utf8"
            )
        file_handle = None
        return file_handle

    def test_defined_in_try_and_except(self):
        try:
            file_handle = open("foo", encoding="utf8")  # must not trigger
        except FileNotFoundError:
            file_handle = open("bar", encoding="utf8")  # must not trigger
        with file_handle:
            return file_handle.read()

    def test_defined_in_try_and_finally(self):
        try:
            file_handle = open("foo", encoding="utf8")  # must not trigger
        except FileNotFoundError:
            Path("foo").touch()
        finally:
            # +1: [used-before-assignment]
            file_handle.open("foo", encoding="utf")  # must not trigger consider-using-with
        with file_handle:
            return file_handle.read()

    def test_defined_in_different_except_handlers(self, a, b):
        try:
            result = a/b
        except ZeroDivisionError:
            logfile = open("math_errors.txt", encoding="utf8")  # must not trigger
            result = "Can't divide by zero"
        except TypeError:
            logfile = open("type_errors.txt", encoding="utf8")  # must not trigger
            result = "Wrong types"
        else:
            logfile = open("results.txt", encoding="utf8")  # must not trigger
        with logfile:
            logfile.write(result)

    def test_multiple_return_statements(self, predicate):
        if predicate:
            return open("foo", encoding="utf8")  # must not trigger
        return open("bar", encoding="utf8")  # must not trigger

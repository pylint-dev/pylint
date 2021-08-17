# pylint: disable=missing-function-docstring, missing-module-docstring, invalid-name, import-outside-toplevel
# pylint: disable=missing-class-docstring, too-few-public-methods, unused-variable, multiple-statements, line-too-long
"""
The functional test for the standard ``open()`` function has to be moved in a separate file,
because PyPy has to be excluded for the tests as the ``open()`` function is uninferable in PyPy.
However, all remaining checks for consider-using-with work in PyPy, so we do not want to exclude
PyPy from ALL functional tests.
"""
from contextlib import contextmanager

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

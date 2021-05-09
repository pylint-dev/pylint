# pylint: disable=missing-function-docstring, missing-module-docstring, invalid-name, import-outside-toplevel
# pylint: disable=missing-class-docstring, too-few-public-methods, unused-variable
"""
The functional test for the standard ``open()`` function has to be moved in a separate file,
because PyPy has to be excluded for the tests as the ``open()`` function is uninferable in PyPy.
However, all remaining checks for consider-using-with work in PyPy, so we do not want to exclude
PyPy from ALL functional tests.
"""
from contextlib import contextmanager


myfile = open("test.txt")  # [consider-using-with]


def test_open():
    fh = open("test.txt")  # [consider-using-with]
    fh.close()

    with open("test.txt") as fh:  # must not trigger
        fh.read()


def test_open_in_enter():
    """Message must not trigger if the resource is allocated in a context manager."""
    class MyContextManager:
        def __init__(self):
            self.file_handle = None

        def __enter__(self):
            self.file_handle = open("foo.txt", "w")  # must not trigger

        def __exit__(self, exc_type, exc_value, traceback):
            self.file_handle.close()


@contextmanager
def test_open_in_with_contextlib():
    """Message must not trigger if the resource is allocated in a context manager."""
    file_handle = open("foo.txt", "w")  # must not trigger
    yield file_handle
    file_handle.close()

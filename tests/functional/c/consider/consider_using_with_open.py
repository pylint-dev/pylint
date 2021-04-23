# pylint: disable=missing-function-docstring, missing-module-docstring, invalid-name, import-outside-toplevel
"""
The functional test for the standard ``open()`` function has to be moved in a separate file,
because PyPy has to be excluded for the tests as the ``open()`` function is uninferable in PyPy.
However, all remaining checks for consider-using-with work in PyPy, so we do not want to exclude
PyPy from ALL functional tests.
"""


def test_open():
    fh = open("test.txt")  # [consider-using-with]
    fh.close()

    with open("test.txt") as fh:  # must not trigger
        fh.read()

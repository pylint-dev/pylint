"""Recursion error for https://github.com/pylint-dev/pylint/issues/2906"""
# pylint: disable=disallowed-name,global-statement,invalid-name,missing-docstring
lst = []


def foo():
    lst.append(0)


def bar():
    global lst

    length = len(lst)
    lst += [length]

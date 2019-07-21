"""Recursion error for https://github.com/PyCQA/pylint/issues/2906"""
# pylint: disable=blacklisted-name,global-statement,invalid-name,missing-docstring
lst = []


def foo():
    lst.append(0)


def bar():
    global lst

    length = len(lst)
    lst += [length]

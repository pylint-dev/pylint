"""Crash regression in astroid on Compare node inference
Fixed in https://github.com/PyCQA/astroid/pull/1185"""
# pylint: disable=missing-docstring, broad-exception-raised


# Reported at https://github.com/PyCQA/pylint/issues/5048
def func(parameter):
    if tuple() + (parameter[1],) in set():
        raise Exception()

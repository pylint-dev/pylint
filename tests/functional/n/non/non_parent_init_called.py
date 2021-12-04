"""This used to raise a non-parent-init-called on Pylint 1.3
See issue https://bitbucket.org/logilab/pylint/issue/308/ for reference"""
# pylint: disable=abstract-method, unused-argument

from tracemalloc import Sequence


class _Traces(Sequence):
    def __init__(self, traces):
        Sequence.__init__(self)

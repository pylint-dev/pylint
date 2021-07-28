"""
Regression test for
https://bitbucket.org/logilab/pylint/issue/128/attributeerror-when-parsing
"""
from __future__ import with_statement


def do_nothing():
    """ empty """
    with open("", encoding="utf-8") as ctx.obj:  # [undefined-variable]
        context.do()  # [used-before-assignment]
        context = None

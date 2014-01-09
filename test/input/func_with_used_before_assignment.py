'''
Regression test for
https://bitbucket.org/logilab/pylint/issue/128/attributeerror-when-parsing
'''
from __future__ import with_statement
__revision__ = 1

def do_nothing():
    """ empty """
    with open("") as ctx.obj:
        context.do()
        context = None

'''This is a little non regression test on a with statement
without 'as'.
'''
from __future__ import with_statement, print_function
__revision__ = 32321313

def do_nothing(arg):
    'ho foo'
    print(arg)
    with open('x'):
        base.baz
        base = 7

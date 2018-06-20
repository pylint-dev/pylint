# pylint: disable=missing-docstring,too-few-public-methods,no-self-use,bad-option-value, useless-object-inheritance
from __future__ import print_function

def myfunc(): # [useless-return]
    print('---- testing ---')
    return

class SomeClass(object):
    def mymethod(self): # [useless-return]
        print('---- testing ---')
        return None

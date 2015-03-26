# pylint: disable=R0903
'''Test that a function is considered a method when looked up through a class.
'''
from __future__ import print_function

class Clazz(object):
    'test class'

    def __init__(self, value):
        self.value = value

def func(arg1, arg2):
    'function that will be used as a method'
    return arg1.value + arg2

Clazz.method = func

print(Clazz(1).method(2))

"""Test function argument checker on __init__

Based on test/input/func_arguments.py
"""
# pylint: disable=C0111,R0903,W0231
__revision__ = ''

class Class1Arg(object):
    def __init__(self, first_argument):
        """one argument function"""

class Class3Arg(object):
    def __init__(self, first_argument, second_argument, third_argument):
        """three arguments function"""

class ClassDefaultArg(object):
    def __init__(self, one=1, two=2):
        """function with default value"""

class Subclass1Arg(Class1Arg):
    pass

class ClassAllArgs(Class1Arg):
    def __init__(self, *args, **kwargs):
        pass

class ClassMultiInheritance(Class1Arg, Class3Arg):
    pass

class ClassNew(object):
    def __new__(cls, first_argument, kwarg=None):
        return first_argument, kwarg

Class1Arg(420)
Class1Arg()
Class1Arg(1337, 347)

Class3Arg(420, 789)
Class3Arg()
Class3Arg(1337, 347, 456)
Class3Arg('bab', 'bebe', None, 5.6)

ClassDefaultArg(1, two=5)
ClassDefaultArg(two=5)

Class1Arg(bob=4)
ClassDefaultArg(1, 4, coin="hello")

ClassDefaultArg(1, one=5)

Subclass1Arg(420)
Subclass1Arg()
Subclass1Arg(1337, 347)

ClassAllArgs()
ClassAllArgs(1, 2, 3, even=4, more=5)

ClassMultiInheritance(1)
ClassMultiInheritance(1, 2, 3)

ClassNew(1, kwarg=1)
ClassNew(1, 2, 3)
ClassNew(one=2)

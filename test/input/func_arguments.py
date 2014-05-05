"""Test function argument checker"""
__revision__ = ''

def decorator(fun):
    """Decorator"""
    return fun


class DemoClass(object):
    """Test class for method invocations."""

    @staticmethod
    def static_method(arg):
        """static method."""
        return arg + arg

    @classmethod
    def class_method(cls, arg):
        """class method"""
        return arg + arg

    def method(self, arg):
        """method."""
        return (self, arg)

    @decorator
    def decorated_method(self, arg):
        """decorated method."""
        return (self, arg)


def function_1_arg(first_argument):
    """one argument function"""
    return first_argument

def function_3_args(first_argument, second_argument, third_argument):
    """three arguments function"""
    return first_argument, second_argument, third_argument

def function_default_arg(one=1, two=2):
    """fonction with default value"""
    return two, one


function_1_arg(420)
function_1_arg()
function_1_arg(1337, 347)

function_3_args(420, 789)
function_3_args()
function_3_args(1337, 347, 456)
function_3_args('bab', 'bebe', None, 5.6)

function_default_arg(1, two=5)
function_default_arg(two=5)
# repeated keyword is syntax error in python >= 2.6:
# tests are moved to func_keyword_repeat_py25- / func_keyword_repeat_py26

function_1_arg(bob=4)
function_default_arg(1, 4, coin="hello")

function_default_arg(1, one=5)

# Remaining tests are for coverage of correct names in messages.
LAMBDA = lambda arg: 1

LAMBDA()

def method_tests():
    """"Method invocations."""
    demo = DemoClass()
    demo.static_method()
    DemoClass.static_method()

    demo.class_method()
    DemoClass.class_method()

    demo.method()
    DemoClass.method(demo)

    demo.decorated_method()
    DemoClass.decorated_method(demo)

# Test a regression (issue #234)
import sys

# pylint: disable=too-few-public-methods
class Text(object):
    """ Regression """

    if sys.version_info > (3,):
        def __new__(cls):
            """ empty """
            return object.__new__(cls)
    else:
        def __new__(cls):
            """ empty """
            return object.__new__(cls)

Text()

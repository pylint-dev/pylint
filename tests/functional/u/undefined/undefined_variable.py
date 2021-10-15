# pylint: disable=missing-docstring, multiple-statements, useless-object-inheritance,import-outside-toplevel
# pylint: disable=too-few-public-methods, no-init, no-self-use,bare-except,broad-except, import-error
from __future__ import print_function

# pylint: disable=wrong-import-position
from typing import TYPE_CHECKING

DEFINED = 1

if DEFINED != 1:
    if DEFINED in (unknown, DEFINED):  # [undefined-variable]
        DEFINED += 1


def in_method(var):
    """method doc"""
    var = nomoreknown  # [undefined-variable]
    assert var

DEFINED = {DEFINED:__revision__}  # [undefined-variable]
# +1:[undefined-variable]
DEFINED[__revision__] = OTHER = 'move this is astroid test'

OTHER += '$'

def bad_default(var, default=unknown2):  # [undefined-variable]
    """function with default arg's value set to an nonexistent name"""
    print(var, default)
    print(xxxx)  # [undefined-variable]
    augvar += 1  # [undefined-variable]
    del vardel  # [undefined-variable]

LMBD = lambda x, y=doesnotexist: x+y  # [undefined-variable]
LMBD2 = lambda x, y: x+z  # [undefined-variable]

try:
    POUET # don't catch me
except NameError:
    POUET = 'something'

try:
    POUETT # [used-before-assignment]
except Exception: # pylint:disable = broad-except
    POUETT = 'something'

try:
    POUETTT # don't catch me
except: # pylint:disable = bare-except
    POUETTT = 'something'

print(POUET, POUETT, POUETTT)


try:
    PLOUF  # [used-before-assignment]
except ValueError:
    PLOUF = 'something'

print(PLOUF)

def if_branch_test(something):
    """hop"""
    if something == 0:
        if xxx == 1:  # [used-before-assignment]
            pass
    else:
        print(xxx)
        xxx = 3


def decorator(arg):
    """Decorator with one argument."""
    return lambda: list(arg)


@decorator(arg=[i * 2 for i in range(15)])
def func1():
    """A function with a decorator that contains a listcomp."""

@decorator(arg=(i * 2 for i in range(15)))
def func2():
    """A function with a decorator that contains a genexpr."""

@decorator(lambda x: x > 0)
def main():
    """A function with a decorator that contains a lambda."""

# Test shared scope.

def test_arguments(arg=TestClass):  # [used-before-assignment]
    """ TestClass isn't defined yet. """
    return arg

class TestClass(Ancestor):  # [used-before-assignment]
    """ contains another class, which uses an undefined ancestor. """

    class MissingAncestor(Ancestor1):  # [used-before-assignment]
        """ no op """

    def test1(self):
        """ It should trigger here, because the two classes
        have the same scope.
        """
        class UsingBeforeDefinition(Empty):  # [used-before-assignment]
            """ uses Empty before definition """
        class Empty(object):
            """ no op """
        return UsingBeforeDefinition

    def test(self):
        """ Ancestor isn't defined yet, but we don't care. """
        class MissingAncestor1(Ancestor):
            """ no op """
        return MissingAncestor1

class Self(object):
    """ Detect when using the same name inside the class scope. """
    obj = Self # [undefined-variable]

class Self1(object):
    """ No error should be raised here. """

    def test(self):
        """ empty """
        return Self1


class Ancestor(object):
    """ No op """

class Ancestor1(object):
    """ No op """

NANA = BAT # [undefined-variable]
del BAT


class KeywordArgument(object):
    """Test keyword arguments."""

    enable = True
    def test(self, is_enabled=enable):
        """do nothing."""

    def test1(self, is_enabled=enabled): # [used-before-assignment]
        """enabled is undefined at this point, but it is used before assignment."""

    def test2(self, is_disabled=disabled): # [undefined-variable]
        """disabled is undefined"""

    enabled = True

    func = lambda arg=arg: arg * arg # [undefined-variable]

    arg2 = 0
    func2 = lambda arg2=arg2: arg2 * arg2

# Don't emit if the code is protected by NameError
try:
    unicode_1
except NameError:
    pass

try:
    unicode_2 # [undefined-variable]
except Exception:
    pass

try:
    unicode_3 # [undefined-variable]
except ValueError:
    pass

# See https://bitbucket.org/logilab/pylint/issue/111/
try: raise IOError(1, "a")
except IOError as err: print(err)


def test_conditional_comprehension():
    methods = ['a', 'b', '_c', '_d']
    my_methods = sum(1 for method in methods
                     if not method.startswith('_'))
    return my_methods


class MyError(object):
    pass


class MyClass(object):
    class MyError(MyError):
        pass


def dec(inp):
    def inner(func):
        print(inp)
        return func
    return inner

# Make sure lambdas with expressions
# referencing parent class do not raise undefined variable
# because at the time of their calling, the class name will
# be populated
# See https://github.com/PyCQA/pylint/issues/704
class LambdaClass:
    myattr = 1
    mylambda = lambda: LambdaClass.myattr

# Need different classes to make sure
# consumed variables don't get in the way
class LambdaClass2:
    myattr = 1
    # Different base_scope scope but still applies
    mylambda2 = lambda: [LambdaClass2.myattr for _ in [1, 2]]

class LambdaClass3:
    myattr = 1
    # Nested default argument in lambda
    # Should not raise error
    mylambda3 = lambda: lambda a=LambdaClass3: a

class LambdaClass4:
    myattr = 1
    mylambda4 = lambda a=LambdaClass4: lambda: a # [undefined-variable]

# Make sure the first lambda does not consume the LambdaClass5 class
# name although the expression is is valid
# Consuming the class would cause the subsequent undefined-variable to be masked
class LambdaClass5:
    myattr = 1
    mylambda = lambda: LambdaClass5.myattr
    mylambda4 = lambda a=LambdaClass5: lambda: a # [undefined-variable]


def nonlocal_in_ifexp():
    import matplotlib.pyplot as plt
    def onclick(event):
        if event:
            nonlocal i
            i += 1
            print(i)
    i = 0
    fig = plt.figure()
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show(block=True)



if TYPE_CHECKING:
    from datetime import datetime


def func_should_fail(_dt: datetime):  # [used-before-assignment]
    pass


# The following should not emit an error.
# pylint: disable=invalid-name
if TYPE_CHECKING:
    from typing_extensions import Literal

    AllowedValues = Literal['hello', 'world']


if TYPE_CHECKING:
    from collections import Counter
    from collections import OrderedDict
else:
    Counter = object
    OrderedDict = object


def tick(counter: Counter, name: str, dictionary: OrderedDict) -> OrderedDict:
    counter[name] += 1
    return dictionary


# pylint: disable=unused-argument
def not_using_loop_variable_accordingly(iterator):
    for iteree in iteree: # [undefined-variable]
        yield iteree
# pylint: enable=unused-argument


class DunderClass:
    def method(self):
        # This name is not defined in the AST but it's present at runtime
        return __class__


def undefined_annotation(a:x): # [undefined-variable]
    if x == 2: # [used-before-assignment]
        for x in [1, 2]:
            pass
    return a


# #3711's comment regression test
lst = []
lst2 = [1, 2, 3]

for item in lst:
    pass

bigger = [
    [
        x for x in lst2 if x > item
    ]
    for item in lst
]


# 3791
@decorator(x for x in range(3))
def decorated1(x):
    print(x)

@decorator(x * x for x in range(3))
def decorated2(x):
    print(x)

@decorator(x)  # [undefined-variable]
@decorator(x * x for x in range(3))
def decorated3(x):
    print(x)

@decorator(x * x * y for x in range(3))  # [undefined-variable]
def decorated4(x):
    print(x)


# https://github.com/PyCQA/pylint/issues/5111
# AssignAttr in orelse block of 'TYPE_CHECKING' shouldn't crash
# Name being assigned must be imported in orelse block
if TYPE_CHECKING:
    pass
else:
    from types import GenericAlias
    object().__class_getitem__ = classmethod(GenericAlias)

# Tests for annotation of variables and potentially undefinition

def value_and_type_assignment():
    """The variable assigned a value and type"""
    variable: int = 2
    print(variable)


def only_type_assignment():
    """The variable never gets assigned a value"""
    variable: int
    print(variable)  # [undefined-variable]


def both_type_and_value_assignment():
    """The variable first gets a type and subsequently a value"""
    variable: int
    variable = 1
    print(variable)


def value_assignment_after_access():
    """The variable gets a value after it has been accessed"""
    variable: int
    print(variable)  # [undefined-variable]
    variable = 1


def value_assignment_from_iterator():
    """The variables gets a value from an iterator"""
    variable: int
    for variable in (1, 2):
        print(variable)

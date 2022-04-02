"""Checks for unnecessary-dunder-call."""
# pylint: disable=too-few-public-methods, undefined-variable, useless-object-inheritance
# pylint: disable=missing-class-docstring, missing-function-docstring

# Test includelisted dunder methods raise lint when manually called.
num_str = some_num.__str__() # [unnecessary-dunder-call]
num_repr = some_num.__add__(2) # [unnecessary-dunder-call]
my_repr = my_module.my_object.__repr__() # [unnecessary-dunder-call]

# Test unknown/user-defined dunder methods don't raise lint.
my_woohoo = my_object.__woohoo__()

# Test allowed dunder methods don't raise lint.
class Foo1(object):
    def __init__(self):
        object.__init__(self)

class Foo2(object):
    def __init__(self):
        super().__init__(self)

class Bar1(object):
    def __new__(cls):
        object.__new__(cls)

class Bar2(object):
    def __new__(cls):
        super().__new__(cls)

class Base:
    @classmethod
    def get_first_subclass(cls):
        for subklass in cls.__subclasses__():
            return subklass
        return object

class PluginBase(object):
    subclasses = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

# Test no lint raised for attributes.
my_instance_name = x.__class__.__name__
my_pkg_version = pkg.__version__

# Allow use of dunder methods on super()
# since there is no alternate method to call them
class MyClass(list):
    def __contains__(self, item):
        print("do some special checks")
        return super().__contains__(item)

# But still flag them in other contexts
MY_TEST_BAD = {1, 2, 3}.__contains__(1) # [unnecessary-dunder-call]
MY_TEST_GOOD = 1 in {1, 2, 3}

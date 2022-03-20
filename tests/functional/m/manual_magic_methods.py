# pylint: disable=too-few-public-methods, missing-docstring, undefined-variable, useless-object-inheritance

# Test includelisted magic methods raise lint when manually called.
num_str = some_num.__str__() # [manual-magic-methods]
num_repr = some_num.__add__(2) # [manual-magic-methods]
my_repr = my_module.my_object.__repr__() # [manual-magic-methods]

# Test unknown/user-defined magic methods don't raise lint.
my_woohoo = my_object.__woohoo__()

# Test allowed magic methods don't raise lint.
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

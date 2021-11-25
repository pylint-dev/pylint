# pylint: disable=missing-docstring, invalid-name, too-few-public-methods, no-self-use, line-too-long, unused-argument, protected-access

class AnotherClass():
    def __test(self):  # [unused-private-member]
        pass

class HasUnusedInClass():
    __my_secret = "I have no secrets"  # [unused-private-member]
    __my_used_secret = "I have no secrets unused"

    @classmethod
    def __private_class_method_unused(cls):  # [unused-private-member]
        print(cls.__my_used_secret)

    @classmethod
    def __private_class_method_used(cls):
        pass

    @staticmethod
    def __private_static_method_unused():  # [unused-private-member]
        pass

    @staticmethod
    def __private_static_method_used():
        pass

    def __init__(self):  # Will not trigger as it begins with __ and ends with __
        self.__instance_secret = "I will never be initialized"  # [unused-private-member]
        self.__another_secret = "hello world"

    def __str__(self):  # Will not trigger as it begins with __ and ends with __
        return "hello"

    def __test(self, x, y, z):  # [unused-private-member]
        fn = HasUnusedInClass.__private_class_method_used
        fn()
        fn2 = HasUnusedInClass.__private_static_method_used
        fn2()

    def __my_print(self, string):
        print(self.__another_secret + string)
        another_obj = AnotherClass()
        another_obj.__test()  # this class's test should still be unused

    def hey(self):  # Will not trigger as it does not begin with __
        self.__my_print("!")

    def __test_fn_as_var(self):
        pass

    def assign_fn_to_var(self):
        fn = self.__test_fn_as_var
        fn()

    def __test_recursive(self):  # [unused-private-member]
        self.__test_recursive()

# False positive: Singleton Pattern
class MyCls:
    __class_var = None

    @classmethod
    def set_class_var(cls, var):
        cls.__class_var = var  # should not emit a message, used in get_class_var()

    @classmethod
    def get_class_var(cls):
        return cls.__class_var


class Bla:
    """Regression test for issue 4638"""

    def __init__(self):
        type(self).__a()
        self.__b()
        Bla.__c()

    @classmethod
    def __a(cls):
        pass

    @classmethod
    def __b(cls):
        pass

    @classmethod
    def __c(cls):
        pass


class Klass:
    """Regression test for 4644"""

    __seventyseven = 77
    __ninetyone = 91

    def __init__(self):
        self.twentyone = 21 * (1 / (self.__seventyseven + 33)) % 100
        self.ninetyfive = Klass.__ninetyone + 4


k = Klass()
print(k.twentyone)
print(k.ninetyfive)

# https://github.com/PyCQA/pylint/issues/4657
# Mutation of class member with cls should not fire a false-positive
class FalsePositive4657:
    """False positivie tests for 4657"""
    __attr_a = None
    __attr_b = 'b'

    @classmethod
    def load_attrs(cls):
        """Load attributes."""
        cls.__attr_a = 'a'

    @property
    def attr_a(self):
        """Get a."""
        return self.__attr_a

    @property
    def attr_b(self):
        """Get b."""
        return self.__attr_b

    # Test cases where we assign self.attr, but try to
    # access cls.attr

    def __init__(self):
        self.__attr_c = "this is an unused private instance attribute"  # [unused-private-member]

    @property
    def attr_c(self):
        """Get c."""
        return cls.__attr_c  # [undefined-variable]


# https://github.com/PyCQA/pylint/issues/4668
# Attributes assigned within __new__() has to be processed as part of the class
class FalsePositive4668:
    # pylint: disable=protected-access, no-member, unreachable

    def __new__(cls, func, *args):
        if args:
            true_obj = super(FalsePositive4668, cls).__new__(cls)
            true_obj.func = func
            true_obj.__args = args  # Do not emit message here
            return true_obj

        false_obj = super(FalsePositive4668, cls).__new__(cls)
        false_obj.func = func
        false_obj.__args = args  # Do not emit message here
        false_obj.__secret_bool = False
        false_obj.__unused = None  # [unused-private-member]
        return false_obj
        # unreachable but non-Name return value
        return 3+4

    def exec(self):
        print(self.__secret_bool)
        return self.func(*self.__args)


# https://github.com/PyCQA/pylint/issues/4673
# Nested functions shouldn't cause a false positive if they are properly used
class FalsePositive4673:
    """ The testing class """

    def __init__(self, in_thing):
        self.thing = False
        self.do_thing(in_thing)

    def do_thing(self, in_thing):
        """ Checks the false-positive condition, sets a property. """
        def __false_positive(in_thing):
            print(in_thing)

        def __true_positive(in_thing):  # [unused-private-member]
            print(in_thing)

        __false_positive(in_thing)
        self.thing = True

    def undo_thing(self):
        """ Unsets a property. """
        self.thing = False

    def complicated_example(self, flag):
        def __inner_1():
            pass

        def __inner_2():
            pass

        def __inner_3(fn):
            return fn

        def __inner_4():  # [unused-private-member]
            pass

        fn_to_return = __inner_1 if flag else __inner_3(__inner_2)
        return fn_to_return


# https://github.com/PyCQA/pylint/issues/4755
# Nested attributes shouldn't cause crash
class Crash4755Context:
    def __init__(self):
        self.__messages = None  # [unused-private-member]

class Crash4755Command:
    def __init__(self):
        self.context = Crash4755Context()

    def method(self):
        self.context.__messages = []
        for message in self.context.__messages:
            print(message)


# https://github.com/PyCQA/pylint/issues/4681
# Accessing attributes of the class using the class name should not result in a false positive
# as long as it is used within the class
class FalsePositive4681:
    __instance = None
    __should_cause_error = None  # [unused-private-member]
    @staticmethod
    def instance():
        if FalsePositive4681.__instance is None:
            FalsePositive4681()
        return FalsePositive4681.__instance

    def __init__(self):
        try:
            FalsePositive4681.__instance = 42  # This should be fine
            FalsePositive4681.__should_cause_error = True  # [unused-private-member]
        except Exception:  # pylint: disable=broad-except
            print("Error")
            FalsePositive4681.__instance = False  # This should be fine
            FalsePositive4681.__should_cause_error = False  # [unused-private-member]

# Accessing attributes of the class using `cls` should not result in a false positive
# as long as it is used within the class
class FalsePositive4681b:
    __instance = None

    @classmethod  # Use class method here
    def instance(cls):
        if cls.__instance is None:
            cls()
        return cls.__instance

    def __init__(self):
        try:
            FalsePositive4681b.__instance = 42  # This should be fine
        except Exception:  # pylint: disable=broad-except
            print("Error")
            FalsePositive4681b.__instance = False  # This should be fine


# https://github.com/PyCQA/pylint/issues/4849
# Accessing private static methods from classmethods via `cls` should not result in a
# false positive
class FalsePositive4849:
    @staticmethod
    def __private_method():
        """Is private and does nothing."""

    # This should already be covered by `HasUnusedInClass`
    @staticmethod
    def __unused_private_method():  # [unused-private-member]
        """Is not used."""

    @classmethod
    def use_private_method(cls):
        """Calls private method."""
        cls.__private_method()  # This should pass


class Pony:
    """https://github.com/PyCQA/pylint/issues/4837"""
    __defaults = {}
    __defaults_set = False

    def __init__(self, value):
        self.value = value

    def __init_defaults(self):  # [unused-private-member]
        if not self.__defaults_set:
            type(self).__defaults = { "fur": "pink" }
            type(self).__defaults_set = True

    def __get_fur_color(self):  # [unused-private-member]
        color = lookup_attribute(self.__defaults, "fur")
        return color


def lookup_attribute(mapping, key):
    return mapping[key]


# Test for regression on checking __class__ attribute
# See: https://github.com/PyCQA/pylint/issues/5261
class Foo:
    __ham = 1

    def method(self):
        print(self.__class__.__ham)

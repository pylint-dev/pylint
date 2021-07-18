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


# Test cases for false-positive reported in #4668
# https://github.com/PyCQA/pylint/issues/4668
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
        return false_obj
        # unreachable but non-Name return value
        return 3+4

    def exec(self):
        print(self.__secret_bool)
        return self.func(*self.__args)

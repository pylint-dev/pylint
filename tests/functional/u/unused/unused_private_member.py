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

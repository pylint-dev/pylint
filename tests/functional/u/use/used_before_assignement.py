"""pylint doesn't see the NameError in this module"""
#pylint: disable=consider-using-f-string, missing-function-docstring
__revision__ = None

MSG = "hello %s" % MSG  # [used-before-assignment]

MSG2 = ("hello %s" %
        MSG2) # [used-before-assignment]


class MyClass:
    """Type annotation or default values for first level methods can't refer to their own class"""
    def incorrect_method(self, other: MyClass) -> bool:  # [used-before-assignment]
        return self == other

    def second_incorrect_method(self, other = MyClass()) -> bool:  # [used-before-assignment]
        return self == other

    def correct_method(self, other: "MyClass") -> bool:
        return self == other

    def second_correct_method(self) -> bool:
        def inner_method(self, other: MyClass) -> bool:
            return self == other

        return inner_method(self, MyClass())

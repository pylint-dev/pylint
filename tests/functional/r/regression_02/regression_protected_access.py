"""Test for the regression on (outer)-class traversal for private methods
MyClass does not have an outerclass which previously crashed the protected-access check
"""
# pylint: disable=too-few-public-methods


class MyClass:
    """Test class"""

    @staticmethod
    def _a_private_method():
        """Private method that references the class itself"""
        return MySecondClass.MyClass._a_private_method()  # [protected-access]


class MySecondClass:
    """Class that uses MyClass"""

    MyClass = MyClass

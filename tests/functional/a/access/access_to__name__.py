# pylint: disable=too-few-public-methods
"""test access to __name__ gives undefined member on new/old class instances
but not on new/old class object
"""


class Aaaa:
    """old class"""
    def __init__(self):
        print(self.__name__)  # [no-member]
        print(self.__class__.__name__)

class NewClass:
    """new class"""

    def __new__(cls, *args, **kwargs):
        print('new', cls.__name__)
        return object.__new__(cls, *args, **kwargs)

    def __init__(self):
        print('init', self.__name__)  # [no-member]

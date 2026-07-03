""" docstring for file clientmodule.py """
from data.suppliermodule_test import Interface, DoNothing, DoNothing2

class Ancestor:
    """ Ancestor method """
    cls_member = DoNothing()

    def __init__(self, value):
        local_variable = 0
        self.attr = 'this method shouldn\'t have a docstring'
        self.__value = value

    def get_value(self):
        """ nice docstring ;-) """
        return self.__value

    def set_value(self, value):
        self.__value = value
        return 'this method shouldn\'t have a docstring'

class Specialization(Ancestor):
    TYPE = 'final class'
    top = 'class'

    def __init__(self, value, _id, relation2: DoNothing2):
        Ancestor.__init__(self, value)
        self._id = _id
        self.relation = DoNothing()
        self.relation2 = relation2

    @classmethod
    def from_value(cls, value: int):
        return cls(value, 0, DoNothing2())

    @staticmethod
    def transform_value(value: int) -> int:
        return value * 2

    def increment_value(self) -> None:
        self.set_value(self.get_value() + 1)

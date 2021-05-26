""" file suppliermodule.py """
from collections import UserDict

class Interface:
    def get_value(self):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

class DoNothing: pass

class MyDict(UserDict): pass

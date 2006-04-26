""" file suppliermodule.py """

class NotImplemented(Exception):
    pass

class Interface:
    def get_value(self):
        raise NotImplemented()

    def set_value(self, value):
        raise NotImplemented()

class DoNothing : pass

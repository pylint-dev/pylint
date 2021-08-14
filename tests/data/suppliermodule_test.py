""" file suppliermodule.py """

class Interface:
    def get_value(self):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

class DoNothing: pass

class DoNothing2: pass

class DoSomething:
    def __init__(self, a_string: str, optional_int: int = None):
        self.my_string = a_string
        self.my_int = optional_int

    def do_it(self, new_int: int) -> int:
        return self.my_int + new_int

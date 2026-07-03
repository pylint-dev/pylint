""" file suppliermodule.py """
from typing import Optional

class Interface:
    def get_value(self):
        raise NotImplementedError

    def set_value(self, value):
        raise NotImplementedError

class CustomException(Exception): pass

class DoNothing: pass

class DoNothing2: pass

class DoSomething:
    def __init__(
            self,
            a_string: str,
            optional_int: int = None,
            optional_int_2: Optional[int] = None):
        self.my_string = a_string
        self.my_int = optional_int
        self.my_int_2 = optional_int_2

    def do_it(self, new_int: int) -> int:
        return self.my_int + new_int

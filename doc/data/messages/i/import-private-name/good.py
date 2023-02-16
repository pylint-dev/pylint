# No error since imports are used as type annotations
from classes import _PrivateClassA, safe_get_A

a_var: _PrivateClassA = safe_get_A()

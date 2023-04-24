""" docstring for file nullable_pattern.py """
from typing import Optional

class NullablePatterns:
    def return_nullable_1(self) -> int | None:
        """ Nullable return type using the | operator as mentioned in PEP 604, see https://peps.python.org/pep-0604 """
        pass

    def return_nullable_2(self) -> Optional[int]:
        pass

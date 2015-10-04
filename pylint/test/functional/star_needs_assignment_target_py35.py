"""
Test PEP 0448 -- Additional Unpacking Generalizations
https://www.python.org/dev/peps/pep-0448/
"""
UNPACK_TUPLE = (*range(4), 4)
UNPACK_LIST = [*range(4), 4]
UNPACK_DICT = {*range(4), 4}

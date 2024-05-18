"""If the stub is preferred over the .py, this might emit not-an-iterable"""
from pyi.foo import three_item_iterable

for val in three_item_iterable():
    print(val)

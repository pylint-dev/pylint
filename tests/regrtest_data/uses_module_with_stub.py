"""If the stub is preferred over the .py, this might emit not-an-iterable"""
from pyi.a_module_that_we_definitely_dont_use_in_the_functional_tests import three_item_iterable

for val in three_item_iterable():
    print(val)

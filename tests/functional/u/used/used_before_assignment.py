"""Miscellaneous used-before-assignment cases"""
# pylint: disable=consider-using-f-string, missing-function-docstring
__revision__ = None


MSG = "hello %s" % MSG  # [used-before-assignment]

MSG2 = "hello %s" % MSG2  # [used-before-assignment]

def outer():
    inner()  # [used-before-assignment]
    def inner():
        pass

outer()

import time  # pylint: disable=unused-import, wrong-import-position
def redefine_time_import():
    print(time.time())  # [used-before-assignment]
    import time  # pylint: disable=import-outside-toplevel, reimported, redefined-outer-name

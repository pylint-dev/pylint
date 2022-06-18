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


# pylint: disable=unused-import, wrong-import-position, import-outside-toplevel, reimported, redefined-outer-name, global-statement
import time
def redefine_time_import():
    print(time.time())  # [used-before-assignment]
    import time


def redefine_time_import_with_global():
    global time  # pylint: disable=invalid-name
    print(time.time())
    import time

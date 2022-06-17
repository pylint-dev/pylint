"""pylint doesn't see the NameError in this module"""
# pylint: disable=consider-using-f-string, missing-function-docstring
__revision__ = None


MSG = "hello %s" % MSG  # [used-before-assignment]

MSG2 = "hello %s" % MSG2  # [used-before-assignment]

def outer():
    inner()  # [used-before-assignment]
    def inner():
        pass

outer()

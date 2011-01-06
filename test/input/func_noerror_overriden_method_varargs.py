# pylint: disable=R0201,R0903
"""docstring"""

__revision__ = 1

class SuperClass(object):
    """docstring"""
    def impl(self, arg1, arg2):
        """docstring"""
        return arg1 + arg2

class MyClass(SuperClass):
    """docstring"""
    def impl(self, *args, **kwargs):
        """docstring"""
        # ...do stuff here...
        super(MyClass, self).impl(*args, **kwargs)

# ...do stuff here...

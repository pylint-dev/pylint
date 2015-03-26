# pylint: disable=R0903
"""use new astroid context sensitive inference"""


class Super(object):
    """super class"""
    def __init__(self):
        self.bla = None

    def instance(cls):
        """factory method"""
        return cls()
    instance = classmethod(instance)

class Sub(Super):
    """dub class"""
    def method(self):
        """specific method"""
        return 'method called', self

# should see the Sub.instance() is returning a Sub instance, not a Super
# instance
Sub.instance().method()

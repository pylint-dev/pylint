# pylint: disable=too-few-public-methods, missing-docstring, no-self-use, useless-object-inheritance

class Abcd(object):

    def __init__(self):
        self.aarg = False

    def abcd(self, aaa=1, bbbb=None):
        return aaa, bbbb

    def args(self):
        self.aarg = True


class Cdef(Abcd):

    def __init__(self, aaa):
        Abcd.__init__(self)
        self.aaa = aaa

    def abcd(self, aaa, bbbb=None): # [signature-differs]
        return aaa, bbbb


class Ghij(Abcd):
    def __init__(self, aaa):
        Abcd.__init__(self)
        self.aaa = aaa

    def abcd(self, *args, **kwargs):
        """Test that a method with variadics does not trigger the warning"""
        return super().abcd(*args, **kwargs)

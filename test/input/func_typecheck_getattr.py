# pylint: disable=
"""check getattr if inference succeed"""

__revision__ = None

class Provider:
    """provide some attributes and method"""
    cattr = 4
    def __init__(self):
        self.attr = 4
    def method(self, val):
        """impressive method"""
        return self.attr * val
    def hophop(self):
        """hop method"""
        print 'hop hop hop', self
    

class Client:
    """use provider class"""
    
    def __init__(self):
        self._prov = Provider()
        self._prov_attr = Provider.cattr
        self._prov_attr2 = Provider.cattribute
        self.set_later = 0

    def set_set_later(self, value):
        """set set_later attribute (introduce an inference ambiguity)"""
        self.set_later = value
        
    def use_method(self):
        """use provider's method"""
        self._prov.hophop()
        self._prov.hophophop()

    def use_attr(self):
        """use provider's attr"""
        print self._prov.attr
        print self._prov.attribute

    def debug(self):
        """print debug information"""
        print self.__class__.__name__
        print self.__doc__
        print self.__dict__
        print self.__module__

    def test_bt_types(self):
        """test access to unexistant member of builtin types"""
        lis = []
        lis.apppend(self)
        dic = {}
        dic.set(self)
        tup = ()
        tup.append(self)
        string = 'toto'
        print string.loower()
        # unicode : moved to func_3k_removed_stuff_py_30.py
        #
        integer = 1
        print integer.whatever

print object.__init__
print property.__init__
print Client().set_later.lower()

# should detect mixing new style / old style classes
Client.__bases__ += (object,) 

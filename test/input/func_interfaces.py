# pylint:disable=R0201
"""docstring"""
__revision__ = ''

class Interface:
    """base class for interfaces"""

class IMachin(Interface):
    """docstring"""
    def truc(self):
        """docstring"""
        
    def troc(self, argument):
        """docstring"""

class Correct1:
    """docstring"""
    __implements__ = IMachin

    def __init__(self):
        pass

    def truc(self):
        """docstring"""
        pass
    
    def troc(self, argument):
        """docstring"""
        pass
    
class Correct2:
    """docstring"""
    __implements__ = (IMachin,)

    def __init__(self):
        pass

    def truc(self):
        """docstring"""
        pass
    
    def troc(self, argument):
        """docstring"""
        print argument

class MissingMethod:
    """docstring"""
    __implements__ = IMachin,

    def __init__(self):
        pass

    def troc(self, argument):
        """docstring"""
        print argument
   
    def other(self):
        """docstring"""
     
class BadArgument:
    """docstring"""
    __implements__ = (IMachin,)

    def __init__(self):
        pass
 
    def truc(self):
        """docstring"""
        pass
    
    def troc(self):
        """docstring"""
        pass
    
class InterfaceCantBeFound:
    """docstring"""
    __implements__ = undefined

    def __init__(self):
        """only to make pylint happier"""
    
    def please(self):
        """public method 1/2"""

    def besilent(self):
        """public method 2/2"""

class InterfaceCanNowBeFound:
    """docstring"""
    __implements__ = BadArgument.__implements__ + Correct2.__implements__

    def __init__(self):
        """only to make pylint happier"""
    
    def please(self):
        """public method 1/2"""

    def besilent(self):
        """public method 2/2"""


class EmptyImplements:
    """no pb"""
    __implements__ = ()
    def __init__(self):
        """only to make pylint happier"""

    def please(self):
        """public method 1/2"""

    def besilent(self):
        """public method 2/2"""



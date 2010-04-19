# pylint: disable=W0232, R0903
"""test max parents"""
__revision__ = None

class Aaaa:
    """yo"""
class Bbbb:
    """yo"""
class Cccc:
    """yo"""
class Dddd:
    """yo"""
class Eeee:
    """yo"""
class Ffff:
    """yo"""
class Gggg:
    """yo"""
class Hhhh:
    """yo"""

class Iiii(Aaaa, Bbbb, Cccc, Dddd, Eeee, Ffff, Gggg, Hhhh):
    """yo"""
    
class Jjjj(Iiii):
    """yo"""
    

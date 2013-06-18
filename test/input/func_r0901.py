# pylint: disable=W0232, R0903
"""test max parents"""
__revision__ = None

class Aaaa(object):
    """yo"""
class Bbbb(object):
    """yo"""
class Cccc(object):
    """yo"""
class Dddd(object):
    """yo"""
class Eeee(object):
    """yo"""
class Ffff(object):
    """yo"""
class Gggg(object):
    """yo"""
class Hhhh(object):
    """yo"""

class Iiii(Aaaa, Bbbb, Cccc, Dddd, Eeee, Ffff, Gggg, Hhhh):
    """yo"""

class Jjjj(Iiii):
    """yo"""


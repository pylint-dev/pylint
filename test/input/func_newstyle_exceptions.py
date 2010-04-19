# pylint: disable=C0103
"""test pb with exceptions and old/new style classes"""

__revision__ = 1

class OkException(Exception):
    """bien bien bien"""
    
class BofException:
    """mouais"""
    
class NewException(object):
    """non si py < 2.5 !"""

def fonctionOk():
    """raise"""
    raise OkException('hop')

def fonctionBof():
    """raise"""
    raise BofException('hop')

def fonctionNew():
    """raise"""
    raise NewException()

def fonctionBof2():
    """raise"""
    raise BofException, 'hop'

def fonctionNew2():
    """raise"""
    raise NewException

def fonctionNotImplemented():
    """raise"""
    raise NotImplemented, 'hop'

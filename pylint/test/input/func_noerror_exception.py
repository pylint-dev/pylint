""" module doc """
__revision__ = ''

class MyException(Exception):
    """a custom exception with its *own* __init__ !!"""
    def __init__(self, msg):
        Exception.__init__(self, msg)

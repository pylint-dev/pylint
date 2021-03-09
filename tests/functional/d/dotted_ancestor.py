"""bla"""
# pylint: disable=no-absolute-import

from . import func_w0233

__revision__ = 'yo'

class Aaaa(func_w0233.AAAA):  # [too-few-public-methods]
    """test dotted name in ancestors"""
    def __init__(self):
        func_w0233.AAAA.__init__(self)

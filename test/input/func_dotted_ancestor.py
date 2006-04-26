"""bla"""

__revision__ = 'yo'


from input import func_w0233

class Aaaa(func_w0233.AAAA):
    """test dotted name in ancestors"""
    def __init__(self):
        func_w0233.AAAA.__init__(self)

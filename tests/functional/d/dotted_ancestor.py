"""bla"""


from ..n.non import non_init_parent_called


class Aaaa(non_init_parent_called.AAAA):  # [too-few-public-methods]
    """test dotted name in ancestors"""
    def __init__(self):
        non_init_parent_called.AAAA.__init__(self)

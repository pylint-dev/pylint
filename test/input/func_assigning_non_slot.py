""" Checks assigning attributes not found in class slots
will trigger assigning-non-slot warning.
"""
# pylint: disable=too-few-public-methods, no-init
from collections import deque

__revision__ = 0

class Empty(object):
    """ empty """

class Bad(object):
    """ missing not in slots. """

    __slots__ = ['member']

    def __init__(self):
        self.missing = 42

class Bad2(object):
    """ missing not in slots """
    __slots__ = [deque.__name__, 'member']

    def __init__(self):
        self.deque = 42
        self.missing = 42

class Bad3(Bad):
    """ missing not found in slots """

    __slots__ = ['component']

    def __init__(self):
        self.component = 42
        self.member = 24
        self.missing = 42
        super(Bad3, self).__init__()

class Good(Empty):
    """ missing not in slots, but Empty doesn't
    specify __slots__.
    """
    __slots__ = ['a']

    def __init__(self):
        self.missing = 42

class Good2(object):
    """ Using __dict__ in slots will be safe. """

    __slots__ = ['__dict__', 'comp']

    def __init__(self):
        self.comp = 4
        self.missing = 5
    
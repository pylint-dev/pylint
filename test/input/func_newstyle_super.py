# pylint: disable=R0903,import-error
"""check use of super"""

from unknown import Missing
__revision__ = None

class Aaaa:
    """old style"""
    def hop(self):
        """hop"""
        super(Aaaa, self).hop()

    def __init__(self):
        super(Aaaa, self).__init__()

class NewAaaa(object):
    """old style"""
    def hop(self):
        """hop"""
        super(NewAaaa, self).hop()

    def __init__(self):
        super(object, self).__init__()

class Py3kAaaa(NewAaaa):
    """new style"""
    def __init__(self):
        super().__init__()

class Py3kWrongSuper(Py3kAaaa):
    """new style"""
    def __init__(self):
        super(NewAaaa, self).__init__()

class WrongNameRegression(Py3kAaaa):
    """ test a regression with the message """
    def __init__(self):
        super(Missing, self).__init__()

class Getattr(object):
    """ crash """
    name = NewAaaa

class CrashSuper(object):
    """ test a crash with this checker """
    def __init__(self):
        super(Getattr.name, self).__init__()

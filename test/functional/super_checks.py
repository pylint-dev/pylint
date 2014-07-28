# pylint: disable=too-few-public-methods,import-error
"""check use of super"""

from unknown import Missing

class Aaaa:  # <3.0:[old-style-class]
    """old style"""
    def hop(self):  # <3.0:[super-on-old-class]
        """hop"""
        super(Aaaa, self).hop()

    def __init__(self):  # <3.0:[super-on-old-class]
        super(Aaaa, self).__init__()

class NewAaaa(object):
    """old style"""
    def hop(self):
        """hop"""
        super(NewAaaa, self).hop()

    def __init__(self):
        super(object, self).__init__()  # [bad-super-call]

class Py3kAaaa(NewAaaa):
    """new style"""
    def __init__(self):
        super().__init__()  # <3.0:[missing-super-argument]

class Py3kWrongSuper(Py3kAaaa):
    """new style"""
    def __init__(self):
        super(NewAaaa, self).__init__()  # [bad-super-call]

class WrongNameRegression(Py3kAaaa):
    """ test a regression with the message """
    def __init__(self):
        super(Missing, self).__init__()  # [bad-super-call]

class Getattr(object):
    """ crash """
    name = NewAaaa

class CrashSuper(object):
    """ test a crash with this checker """
    def __init__(self):
        super(Getattr.name, self).__init__()  # [bad-super-call]

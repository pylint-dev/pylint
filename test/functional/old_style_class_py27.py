""" Tests for old style classes. """
# pylint: disable=no-init, too-few-public-methods, invalid-name

class Old: # [old-style-class]
    """ old style class """

class Child(Old): # [old-style-class]
    """ still an old style class """

__metaclass__ = type

class NotOldStyle:
    """ Because I have a metaclass at global level. """

class NotOldStyle2:
    """ Because I have a metaclass at class level. """
    __metaclass__ = type

"""test class decorator are recognized"""
#  pylint: disable=R0903,W0232,C,no-absolute-import

from logilab.common.deprecation import deprecated, class_moved

@deprecated('This is a bad class name; use %s to rename'  % class_moved)
class Foo:
    '''foo goo'''

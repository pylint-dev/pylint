# pylint: disable=R0903
"""test attribute access on metaclass"""


__revision__ = 'yo'

class Meta(type):
    """the meta class"""
    def __init__(mcs, name, bases, dictionary):
        super(Meta, mcs).__init__(name, bases, dictionary)
        print mcs, mcs._meta_args
        delattr(mcs, '_meta_args')

class Test(object):
    """metaclassed class"""
    __metaclass__ = Meta
    _meta_args = ('foo', 'bar')

    def __init__(self):
        print '__init__', self

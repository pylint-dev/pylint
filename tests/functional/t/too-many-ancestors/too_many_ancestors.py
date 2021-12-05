# pylint: disable=missing-docstring, too-few-public-methods, useless-object-inheritance, arguments-differ
from collections.abc import MutableSequence

class Aaaa(object):
    pass
class Bbbb(object):
    pass
class Cccc(object):
    pass
class Dddd(object):
    pass
class Eeee(object):
    pass
class Ffff(object):
    pass
class Gggg(object):
    pass
class Hhhh(object):
    pass

class Iiii(Aaaa, Bbbb, Cccc, Dddd, Eeee, Ffff, Gggg, Hhhh): # [too-many-ancestors]
    pass

class Jjjj(Iiii): # [too-many-ancestors]
    pass


# https://github.com/PyCQA/pylint/issues/4166
# https://github.com/PyCQA/pylint/issues/4415
class ItemSequence(MutableSequence):
    """Minimal MutableSequence."""
    def __getitem__(self, key):
        return key

    def __setitem__(self, key, value):
        _ = key, value

    def __delitem__(self, key):
        _ = key

    def insert(self, index, value):
        _ = index, value

    def __len__(self):
        return 1

# pylint: disable=missing-docstring, too-few-public-methods, arguments-differ
from collections.abc import MutableSequence

class Aaaa:
    pass
class Bbbb:
    pass
class Cccc:
    pass
class Dddd:
    pass
class Eeee:
    pass
class Ffff:
    pass
class Gggg:
    pass
class Hhhh:
    pass

class Iiii(Aaaa, Bbbb, Cccc, Dddd, Eeee, Ffff, Gggg, Hhhh): # [too-many-ancestors]
    pass

class Jjjj(Iiii): # [too-many-ancestors]
    pass


# https://github.com/pylint-dev/pylint/issues/4166
# https://github.com/pylint-dev/pylint/issues/4415
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

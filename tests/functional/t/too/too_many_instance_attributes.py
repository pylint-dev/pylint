# pylint: disable=missing-docstring, too-few-public-methods

# Disabled because of a bug with pypy 3.8 see
# https://github.com/PyCQA/pylint/pull/7918#issuecomment-1352737369
# pylint: disable=multiple-statements


class Aaaa: # [too-many-instance-attributes]

    def __init__(self):
        self.aaaa = 1
        self.bbbb = 2
        self.cccc = 3
        self.dddd = 4
        self.eeee = 5
        self.ffff = 6
        self.gggg = 7
        self.hhhh = 8
        self.iiii = 9
        self.jjjj = 10
        self._aaaa = 1
        self._bbbb = 2
        self._cccc = 3
        self._dddd = 4
        self._eeee = 5
        self._ffff = 6
        self._gggg = 7
        self._hhhh = 8
        self._iiii = 9
        self._jjjj = 10
        self.tomuch = None

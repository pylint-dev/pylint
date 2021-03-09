# pylint: disable=missing-docstring
class Data:
    def __init__(self):
        self.shape = [None, 17]

    @property
    def ndim(self):
        return len(self.shape)

    def copy_move_axis(self, old_axis):
        if old_axis < 0:
            old_axis += self.ndim
            assert old_axis >= 0
        assert 0 <= old_axis < self.ndim

        new_shape = [None] * self.ndim
        self.shape = new_shape
        return self

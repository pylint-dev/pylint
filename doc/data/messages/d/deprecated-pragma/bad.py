# pylint: disable-msg=eval-used # [deprecated-pragma]

class Class:
    @property
    @classmethod
    def func(cls):
        pass


if Class.func:
    pass

# pylint: disable-msg=eval-used # [deprecated-pragma]

class CatClass:
    @property
    @classmethod
    def func(cls):
        pass


if CatClass.func:
    pass

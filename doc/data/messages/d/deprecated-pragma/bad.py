# pylint: disable-msg=too-few-public-methods,using-constant-test # [deprecated-pragma]

class Class:
    @property
    @classmethod
    def func(cls):
        pass


if Class.func:
    pass

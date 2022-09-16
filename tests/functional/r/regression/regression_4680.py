# pylint: disable=missing-docstring,too-few-public-methods

import foo.sub  # [import-error]


class Failed(metaclass=foo.sub.Metaclass):
    pass


class FailedTwo(metaclass=ab.ABCMeta):  # [undefined-variable]
    pass


class FailedThree(metaclass=foo.sob.Metaclass):
    pass


assert foo.sub.value is None

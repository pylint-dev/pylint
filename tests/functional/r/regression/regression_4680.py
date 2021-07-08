# pylint: disable=missing-docstring,too-few-public-methods

import pkg.sub  # [import-error]


class Failed(metaclass=pkg.sub.Metaclass):
    pass


class FailedTwo(metaclass=ab.ABCMeta):  # [undefined-variable]
    pass


class FailedThree(metaclass=pkg.sob.Metaclass):
    pass


assert pkg.sub.value is None

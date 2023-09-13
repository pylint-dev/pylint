# pylint: disable=missing-docstring, too-few-public-methods,pointless-statement
# pylint: disable=expression-not-assigned

class MetaIterable(type):
    __iter__ = None


class MetaOldIterable(type):
    __getitem__ = None


class MetaContainer(type):
    __contains__ = None


class NonIterableClass(metaclass=MetaOldIterable):
    __contains__ = None


class OldNonIterableClass(metaclass=MetaOldIterable):
    __contains__ = None


class NonContainerClass(metaclass=MetaContainer):
    __iter__ = None


class MultipleAssignmentNonesClass(metaclass=MetaContainer):
    __len__, __iter__ = [None, None]


class MultipleAssignmentLambdasClass(metaclass=MetaContainer):
    """https://github.com/pylint-dev/pylint/issues/6366"""
    __len__, __iter__ = [lambda x: x] * 2


def test():
    1 in NonIterableClass  # [unsupported-membership-test]
    1 in OldNonIterableClass  # [unsupported-membership-test]
    1 in NonContainerClass # [unsupported-membership-test]
    1 in NonIterableClass()  # [unsupported-membership-test]
    1 in OldNonIterableClass()  # [unsupported-membership-test]
    1 in NonContainerClass()  # [unsupported-membership-test]
    1 in MultipleAssignmentNonesClass()  # [unsupported-membership-test]
    1 in MultipleAssignmentLambdasClass()

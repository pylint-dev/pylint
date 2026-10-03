# [missing-module-docstring]
# pylint: disable=too-few-public-methods


class ClassDocumented:
    """It has a docstring."""


class UndocumentedClass:  # [missing-class-docstring]
    pass


# pylint: disable=missing-class-docstring
class ClassUndocumented:
    pass


# pylint: enable=missing-class-docstring
class OtherClassUndocumented:  # [missing-class-docstring]
    pass


def public_documented():
    """It has a docstring."""


def _private_undocumented():
    # Doesn't need a docstring
    pass


def _private_documented():
    """It has a docstring."""


def public_undocumented():  # [missing-function-docstring]
    pass


# pylint: disable=missing-function-docstring
def undocumented_function():
    pass


# pylint: enable=missing-function-docstring
def undocumented_other_function():  # [missing-function-docstring]
    pass

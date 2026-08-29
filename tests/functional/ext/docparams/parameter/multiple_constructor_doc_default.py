# pylint: disable=missing-module-docstring, too-few-public-methods


def __init__(value: int) -> int:
    """Module-level function named like a constructor.

    Args:
        value: not a class constructor parameter.
    """
    return value


class ConstructorDocsInClassAndInit:  # [multiple-constructor-doc]
    """Class summary.

    Args:
        value: documented in class.
    """

    def __init__(self, value: int) -> None:
        """Initialize.

        Args:
            value: documented in __init__.
        """
        self.value = value


class ConstructorDocsInClassAndNew:  # [multiple-constructor-doc]
    """Class summary.

    Args:
        value: documented in class.
    """

    def __new__(cls, value: int):
        """Create instance.

        Args:
            value: documented in __new__.
        """
        instance = super().__new__(cls)
        instance.value = value
        return instance

# pylint: disable=missing-module-docstring, too-few-public-methods


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

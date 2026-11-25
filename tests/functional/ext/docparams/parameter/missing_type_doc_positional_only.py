"""Tests for missing-type-doc with positional-only parameters, where an annotation
documents the type (#11843).
"""
# pylint: disable=unused-argument


def unannotated_positional_only(param1, /, param2: int):  # [missing-type-doc]
    """The message names param1, not param2.

    Parameters
    ----------
    param1
        A parameter.
    param2
        A parameter.
    """


def annotated_positional_only(param1: int, /, param2: int):
    """Both parameters are annotated.

    Parameters
    ----------
    param1
        A parameter.
    param2
        A parameter.
    """


class MyClass:
    """A class."""

    def self_positional_only(self, /, param1: int, param2: int):
        """Both parameters are annotated.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """

    def unannotated_second(self, /, param1: int, param2):  # [missing-type-doc]
        """The message names param2.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """

    def all_positional_only(self, param1, param2: int, /):  # [missing-type-doc]
        """The message names param1.

        Parameters
        ----------
        param1
            A parameter.
        param2
            A parameter.
        """

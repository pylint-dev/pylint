"""Disabling a message that is incompatible with useless-suppression
never raises useless-suppression, even when nothing was suppressed."""
# pylint: enable=useless-suppression

FIRST = 1  # pylint: disable=cyclic-import
SECOND = 2  # pylint: disable=deprecated-module
THIRD = 3  # pylint: disable=deprecated-method
FOURTH = 4  # pylint: disable=deprecated-argument
FIFTH = 5  # pylint: disable=deprecated-class
SIXTH = 6  # pylint: disable=deprecated-decorator
SEVENTH = 7  # pylint: disable=duplicate-code
EIGHTH = 8  # pylint: disable=unused-variable # [useless-suppression]

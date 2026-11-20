"""Test deprecated-attribute"""

import calendar
import sys

print(calendar.January)  # [deprecated-attribute]


def keep_in_sync(error):
    """The deprecated attributes are kept for compatibility with sys.last_exc."""
    try:
        del sys.last_type
        del sys.last_value
        del sys.last_traceback
        del sys.last_exc
    except AttributeError:
        pass
    sys.last_type = type(error)
    sys.last_value = error
    sys.last_traceback = error.__traceback__
    if sys.version_info >= (3, 12):
        sys.last_exc = error


def without_replacement(error):
    """Nothing sets or deletes sys.last_exc here."""
    del sys.last_type  # [deprecated-attribute]
    sys.last_value = error  # [deprecated-attribute]
    print(sys.last_traceback)  # [deprecated-attribute]


def replacement_deleted_only(error):
    """Deleting sys.last_exc does not excuse setting the deprecated attribute."""
    del sys.last_exc
    sys.last_value = error  # [deprecated-attribute]


def replacement_in_nested_function(error):
    """The replacement must be set in the same function."""
    sys.last_value = error  # [deprecated-attribute]

    def nested():
        sys.last_exc = error

    return nested

"""Test that `break` and `continue` are caught inside the `finally` of a `try/except*`."""

# pylint: disable=missing-docstring, lost-exception


def nested_in_finally(items):
    for item in items:
        try:
            pass
        except* ValueError:
            pass
        finally:
            if item:
                continue  # [continue-in-finally]
            break  # [break-in-finally]

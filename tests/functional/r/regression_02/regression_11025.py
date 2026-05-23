"""Regression test for https://github.com/pylint-dev/pylint/issues/11025

Pylint crashed in the variables checker with::

    TypeError: NotImplemented should not be used in a boolean context

when ``NotImplemented`` appeared as an ``if`` test, because
``bool(NotImplemented)`` raises ``TypeError`` on Python 3.12+.
"""


if NotImplemented:
    x = 1  # pylint: disable=invalid-name
x  # [pointless-statement, possibly-used-before-assignment]

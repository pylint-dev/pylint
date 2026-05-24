"""Regression test for https://github.com/pylint-dev/pylint/issues/11025.

Using ``NotImplemented`` as an ``if`` test crashed the variables checker
because ``not NotImplemented`` raises a ``TypeError`` in a boolean context
on Python 3.14.
"""

if NotImplemented:
    VALUE = 1

print(VALUE)  # [possibly-used-before-assignment]

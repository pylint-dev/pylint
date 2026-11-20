"""Regression test for https://github.com/pylint-dev/pylint/issues/1498

On the right of ``value is None or ...``, ``value`` is not None: the
subscript there is fine. Fixed in astroid by pylint-dev/astroid#3101.
"""

# pylint: disable=missing-docstring

value = None
while True:
    if value is None or value["count"] == 0:
        value = {"count": 1}
    else:
        break
print(value)

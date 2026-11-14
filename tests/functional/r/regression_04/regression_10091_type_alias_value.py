"""Regression test for https://github.com/pylint-dev/pylint/issues/10091

The name of a ``type`` statement is a ``TypeAliasType``, which has a
``__value__``, not the aliased class.
"""

type Text = str

print(Text.__value__)

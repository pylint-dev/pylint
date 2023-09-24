"""Test the generated-members config option."""
# pylint: disable=pointless-statement, invalid-name
from __future__ import annotations
from astroid import nodes
from pylint import checkers

class Klass:
    """A class with a generated member."""

print(Klass().DoesNotExist)
print(Klass().aBC_set1)
print(Klass().ham.does.not_.exist)
print(Klass().spam.does.not_.exist)  # [no-member]
nodes.Tuple.does.not_.exist
checkers.base.doesnotexist()

session = Klass()
SESSION = Klass()
session.rollback()
SESSION.rollback()


# https://github.com/pylint-dev/pylint/issues/6594
# Don't emit no-member inside type annotations
# with PEP 563 'from __future__ import annotations'
print(Klass.X)  # [no-member]
var: "Klass.X"
var2: Klass.X

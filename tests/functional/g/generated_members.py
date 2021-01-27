"""Test the generated-members config option."""
# pylint: disable=pointless-statement, invalid-name, useless-object-inheritance
from __future__ import print_function
from astroid import node_classes
from pylint import checkers

class Klass(object):
    """A class with a generated member."""

print(Klass().DoesNotExist)
print(Klass().aBC_set1)
print(Klass().ham.does.not_.exist)
print(Klass().spam.does.not_.exist)  # [no-member]
node_classes.Tuple.does.not_.exist
checkers.base.doesnotexist()

session = Klass()
SESSION = Klass()
session.rollback()
SESSION.rollback()

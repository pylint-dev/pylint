"""Test the generated-members config option."""
from __future__ import print_function

class Klass(object):
    """A class with a generated member."""

print(Klass().DoesNotExist)
print(Klass().aBC_set1)

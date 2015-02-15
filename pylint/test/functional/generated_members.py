"""Test the generated-members config option."""

class Klass(object):
    """A class with a generated member."""

print Klass().DoesNotExist
print Klass().aBC_set1

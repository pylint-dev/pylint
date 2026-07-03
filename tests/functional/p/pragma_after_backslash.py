"""Test that a pragma has an effect when separated by a backslash."""
# pylint: disable=too-few-public-methods

class Foo:
    """block-disable test"""

    def meth3(self):
        """test one line disabling"""
        print(self.bla) \
           # pylint: disable=no-member

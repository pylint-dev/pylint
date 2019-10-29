"""Test that a noqa pragma has an effect."""
# pylint: disable=too-few-public-methods

class Foo:
    """block-disable test"""

    def meth3(self):
        """test one line disabling"""
        print(self.bla)  # noqa: E1101

        print(self.bla)  # noqa: no-member

        self.thing = self.bla  # noqa: E1101, attribute-defined-outside-init

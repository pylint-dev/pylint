""" Non ASCII char in class name

Note that the end line parameter here seems to be off.
We would expect it to be the same as the start, as we only refer
to the class Name and not the complete class definition.
But this is not possible atm with pylint.
"""
# pylint: disable=too-few-public-methods


class НoldIt:  # [non-ascii-name]
    """Nice class."""

    def public(self):
        """do something"""
        print(self)


def main():
    """Main function"""
    # Usage should not raise a second error
    foobar = НoldIt()
    print(foobar)

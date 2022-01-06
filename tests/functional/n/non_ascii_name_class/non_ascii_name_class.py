""" Non ASCII char in class name """
# pylint: disable=too-few-public-methods


class НoldIt:  # [non-ascii-identifier]
    """nice classs"""

    def public(self):
        """do something"""
        print(self)


def main():
    """Main function"""
    # Usage should not raise a second error
    foobar = НoldIt()
    print(foobar)

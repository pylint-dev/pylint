"""Non ASCII name in class variable"""


class OkayIsh:
    """Class docstring"""

    def public(self):
        """Be public!"""
        print(self)

    def __init__(self):
        self.łoopback = "invalid"  # [non-ascii-name]

    def foobar(self):
        """do something"""
        # Usage should not raise a second error
        return self.łoopback

def main():
    """main function"""
    # Usage should not raise a second error
    barrrr = OkayIsh()
    barrrr.foobar()
    test = barrrr.łoopback
    print(test)

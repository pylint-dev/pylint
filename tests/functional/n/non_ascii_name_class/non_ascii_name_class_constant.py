"""non ASCII name in global class variable/class constant"""


class OkayIsh:
    """Class docstring"""
    ŁOOPBACK = "invalid"  # [non-ascii-name]


    def more_public(self):
        """yet another public method"""
        print(self)

    def public(self):
        """something public"""
        print(self)



def main():
    """Main func"""
    # Usage should not raise a second error
    foobar = OkayIsh.ŁOOPBACK
    print(foobar)

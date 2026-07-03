"""invalid ascii char in a for loop"""
# pylint: disable=consider-using-join
import os


def main():
    """main func"""
    # +2: [non-ascii-name]
    a_variable = ""
    for łol in os.listdir("."):
        # Usage should not raise a second error
        a_variable += (
            f"{łol}                                                                       "
        )

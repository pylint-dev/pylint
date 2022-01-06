"""invalid ascii char in a for loop"""

import os


def main():
    """main func"""
    # +2: [non-ascii-identifier]
    a_variable = ""
    for łol in os.listdir("."):
        # Usage should not raise a second error
        a_variable += (
            f"{łol}                                                                       "
        )

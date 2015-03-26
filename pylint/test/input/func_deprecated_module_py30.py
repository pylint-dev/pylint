"""test deprecated module
"""

from __future__ import print_function


if True:
    import optparse
    print(optparse)
    # false positive (#10061)
    import stringfile
    print(stringfile)

"""test deprecated module
"""
from __future__ import absolute_import, print_function
__revision__ = 0


if __revision__:
    import Bastion
    print(Bastion)
    # false positive (#10061)
    import stringfile
    print(stringfile)

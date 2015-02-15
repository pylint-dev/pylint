# pylint: disable=R0903,W0403
"""package's __init__ file"""

__revision__ = 0

# E0602 - Undefined variable '__path__'
__path__ += "folder"

class AudioTime(object):
    """test precedence over the AudioTime submodule"""

    DECIMAL = 3

import subpackage

"""test cyclic import
"""

from __future__ import print_function

from . import w0401_cycle  # pylint: disable=cyclic-import

if w0401_cycle:
    print(w0401_cycle)

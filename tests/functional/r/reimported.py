# pylint: disable=missing-docstring,unused-import,import-error, wildcard-import,unused-wildcard-import,redefined-builtin,no-name-in-module,ungrouped-imports,wrong-import-order

from time import sleep, sleep  # [reimported]
from lala import missing, missing  # [reimported]

import missing1
import missing1 # [reimported]

from collections import deque
from itertools import deque # [reimported]

from collections import OrderedDict
from itertools import OrderedDict as NotOrderedDict

from itertools import *
from os import *

# pylint: disable=misplaced-future
from __future__ import absolute_import, print_function

import sys

import xml.etree.ElementTree
from xml.etree import ElementTree  # [reimported]

from email import encoders
import email.encoders  # [reimported]

import sys  # [reimported]  #pylint: disable=ungrouped-imports,wrong-import-order
__revision__ = 0

def no_reimport():
    """docstring"""
    import os  #pylint: disable=import-outside-toplevel
    print(os)


def reimport():
    """This function contains a reimport."""
    import sys  # [reimported,redefined-outer-name] #pylint: disable=import-outside-toplevel
    del sys


del sys, ElementTree, xml.etree.ElementTree, encoders, email.encoders

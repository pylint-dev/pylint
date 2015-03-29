"""unused import"""
# pylint: disable=undefined-all-variable, import-error, no-absolute-import, too-few-public-methods, missing-docstring
import xml.etree  # [unused-import]
import xml.sax  # [unused-import]
import os.path as test  # [unused-import]
from sys import argv as test2  # [unused-import]
from sys import flags  # [unused-import]
# +1:[unused-import,unused-import]
from collections import deque, OrderedDict, Counter
DATA = Counter()

from fake import SomeName
class SomeClass(object):
    SomeName = SomeName # https://bitbucket.org/logilab/pylint/issue/475

from never import __all__

"""This should not emit a super-init-not-called warning. It previously did this, because
``next(node.infer())`` was used in that checker's logic and the first inferred node
was an Uninferable object, leading to this false positive."""
# pylint: disable=too-few-public-methods

import ctypes


class Foo(ctypes.BigEndianStructure):
    """A class"""

    def __init__(self):
        ctypes.BigEndianStructure.__init__(self)

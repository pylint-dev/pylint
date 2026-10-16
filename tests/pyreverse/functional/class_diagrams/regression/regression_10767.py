# The namedtuple and argparse brains add ``EmptyNode`` instance attributes:
# they must not crash the relationship handlers, and must still show up as
# attributes.
import argparse
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Shape:
    def __init__(self):
        self.origin = Point(0, 0)
        self.options = argparse.Namespace(color="red")

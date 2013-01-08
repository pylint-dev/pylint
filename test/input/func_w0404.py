"""Unittests for W0404 (reimport)"""

__revision__ = 0

import sys

import xml.etree.ElementTree
from xml.etree import ElementTree

from multiprocessing import pool
import multiprocessing.pool

import sys

def no_reimport():
    """docstring"""
    import os
    print os


def reimport():
    """This function contains a reimport."""
    import sys
    del sys


del sys, ElementTree, xml.etree.ElementTree, pool, multiprocessing.pool

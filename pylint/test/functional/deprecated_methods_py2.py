""" Functional test for deprecated methods in Python 2 """
# pylint: disable=no-member,missing-docstring
import os
import xml.etree.ElementTree
import unittest

os.popen2('')     # [deprecated-method]
os.popen3('')     # [deprecated-method]
os.popen4('')     # [deprecated-method]
xml.etree.ElementTree.Element('elem').getchildren()     # [deprecated-method]


class Tests(unittest.TestCase):

    def test_foo(self):
        self.assertEquals(2 + 2, 4)  # [deprecated-method]
        self.assertNotEquals(2 + 2, 4)  # [deprecated-method]
        self.assertAlmostEquals(2 + 2, 4)  # [deprecated-method]
        self.assertNotAlmostEquals(2 + 2, 4)  # [deprecated-method]
        self.assert_("abc" == "2")  # [deprecated-method]

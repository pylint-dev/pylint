""" Functional tests for method deprecation. """
# pylint: disable=missing-docstring, super-init-not-called, not-callable
import base64
import inspect
import logging
import nntplib
import unittest
import xml.etree.ElementTree


class MyTest(unittest.TestCase):
    def test(self):
        self.assert_(True)  # [deprecated-method]

xml.etree.ElementTree.Element('tag').getchildren()  # [deprecated-method]
xml.etree.ElementTree.Element('tag').getiterator()  # [deprecated-method]
nntplib.NNTP(None).xpath(None) # [deprecated-method]


inspect.getargspec(None) # [deprecated-method]
logging.warn("a") # [deprecated-method]
base64.encodestring("42") # [deprecated-method]
base64.decodestring("42") # [deprecated-method]


class SuperCrash(unittest.TestCase):

    def __init__(self):
        # should not crash.
        super()()

xml.etree.ElementTree.iterparse(None)


class Tests(unittest.TestCase):

    def test_foo(self):
        self.assertEquals(2 + 2, 4)  # [deprecated-method]
        self.assertNotEquals(2 + 2, 4)  # [deprecated-method]
        self.assertAlmostEquals(2 + 2, 4)  # [deprecated-method]
        self.assertNotAlmostEquals(2 + 2, 4)  # [deprecated-method]
        self.assert_("abc" == "2")  # [deprecated-method]

        self.assertRaisesRegex(ValueError, "exception")
        self.assertRegex("something", r".+")

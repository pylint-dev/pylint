import unittest


class DummyTestCase(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue("foo")  # [redundant-unittest-assert]

import unittest


class DummyTestCase(unittest.TestCase):
    def test_dummy(self):
        value = "foo"

        self.assertTrue(value)

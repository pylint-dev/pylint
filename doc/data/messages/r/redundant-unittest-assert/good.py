import unittest


class DummyTestCase(unittest.TestCase):
    def test_dummy(self):
        actual = "test_result"
        self.assertEqual(actual, "expected")

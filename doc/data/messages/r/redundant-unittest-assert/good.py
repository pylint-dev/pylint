import unittest


class DummyTestCase(unittest.TestCase):
    def test_dummy(self):
        # Nothing, as an assert of a string literal will always pass
        pass

def test_division():
    a = 9 / 3
    assert a == 3

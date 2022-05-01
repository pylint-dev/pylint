import unittest


class DummyTestCase(unittest.TestCase):
    def test_dummy(self):
        self.assertTrue("foo")  # [redundant-unittest-assert]


def test_division():
    a = 9 / 3
    assert "No ZeroDivisionError were raised"  # assert-on-string-literal

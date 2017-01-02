# coding: utf-8
"""Test Except Pass usage"""
# pylint: disable=too-few-public-methods, no-self-use


class TestExceptPass(object):
    """Test Except Pass class """

    def test_method(self):
        """Test method """
        try:
            raise Exception('Exception')
        except Exception:
            pass  # [except-pass]

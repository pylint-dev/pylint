# coding: utf-8
"""Test Except Pass usage"""
# pylint: disable=too-few-public-methods, no-self-use, continue-in-finally
# pylint: disable=undefined-variable, bare-except, continue-in-finally
# pylint: disable=bad-except-order
# pylint: disable=import-error
# pylint: disable=ungrouped-imports, redefine-in-handler
# pylint: disable=too-many-nested-blocks, misplaced-bare-raise
# pylint: disable=redefined-argument-from-local
# pylint: disable=no-name-in-module, unnecessary-pass
# pylint: disable=redefined-argument-from-local
# pylint: disable=undefined-variable, bare-except, continue-in-finally
# pylint: disable=bad-except-order, no-member, wrong-import-position
# pylint: disable=undefined-variable


class TestExceptPass(object):
    """Test Except Pass class """

    def test_method(self):
        """Test method """
        try:
            raise Exception('Exception')
        except Exception:
            pass  # [except-pass]

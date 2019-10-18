"""Check that we do not crash with a recursion error"""
import setuptools


# pylint: disable=missing-docstring,too-few-public-methods
class Custom(setuptools.Command):
    pass

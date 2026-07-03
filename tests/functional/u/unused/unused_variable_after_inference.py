"""Regression test for https://github.com/pylint-dev/pylint/issues/6895"""
# pylint: disable=missing-class-docstring,too-few-public-methods
import argparse
class Cls:
    def meth(self):
        """Enable non-iterator-returned to produce the failure condition"""
        return argparse.Namespace(debug=True)

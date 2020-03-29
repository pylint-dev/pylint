""" Here we test the executable iterfaces shipped with pylint """
import os
import sys
import unittest
from unittest.mock import patch

from pylint import run_pylint, run_epylint, run_pyreverse, run_symilar


class TestRunners(unittest.TestCase):
    """ A tester to ensure that the runners we ship execute with minimal params """

    def test_run_pylint(self):
        """ Tests basic invocation of the pylint setup via the runner func """
        filepath = os.path.abspath(__file__)
        testargs = ["", filepath]
        with patch.object(sys, "argv", testargs):
            with self.assertRaises(SystemExit) as err:
                run_pylint()
            self.assertEqual(0, err.exception.code)

    def test_run_epylint(self):
        """ Tests basic invocation of the epylint setup via its runner func """
        filepath = os.path.abspath(__file__)
        testargs = ["", filepath]
        with patch.object(sys, "argv", testargs):
            with self.assertRaises(SystemExit) as err:
                run_epylint()
            self.assertEqual(0, err.exception.code)

    def test_run_pyreverse(self):
        """ Tests basic invocation of pyreverse """
        filepath = os.path.abspath(__file__)
        testargs = ["", filepath]
        with patch.object(sys, "argv", testargs):
            with self.assertRaises(SystemExit) as err:
                run_pyreverse()
            self.assertEqual(0, err.exception.code)

    def test_run_symilar(self):
        """ Tests basic invocation of the similar utilities via its runner func  """
        filepath = os.path.abspath(__file__)
        testargs = ["", filepath]
        with patch.object(sys, "argv", testargs):
            with self.assertRaises(SystemExit) as err:
                run_symilar()
            self.assertEqual(0, err.exception.code)

"""Test deprecated functions of the standard library, deprecated in Python 3.13."""
# pylint: disable=missing-function-docstring

import glob

glob.glob0(".", "x")  # [deprecated-method]
glob.glob1(".", "*")  # [deprecated-method]
glob.glob("*")

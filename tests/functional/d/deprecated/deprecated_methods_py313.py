"""Test methods deprecated in Python 3.13."""
import glob
from glob import glob1

glob.glob0(".", "x")  # [deprecated-method]
glob1(".", "*")  # [deprecated-method]
glob.glob("*", root_dir=".")

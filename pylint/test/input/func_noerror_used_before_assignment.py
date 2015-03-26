# pylint: disable = line-too-long, multiple-statements, missing-module-attribute
"""https://bitbucket.org/logilab/pylint/issue/111/false-positive-used-before-assignment-with"""
from __future__ import print_function
try: raise IOError(1, "a")
except IOError as err: print(err)

# pylint: disable = line-too-long, multiple-statements, missing-module-attribute, print-statement
"""https://bitbucket.org/logilab/pylint/issue/111/false-positive-used-before-assignment-with"""

try: raise IOError(1, "a")
except IOError, err: print err

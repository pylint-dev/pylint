"""Tests for inconsistent-mro."""
# pylint: disable=missing-docstring,too-few-public-methods,unused-import,wrong-import-position

class Str(str):
    pass


class Inconsistent(str, Str): # [inconsistent-mro]
    pass


# Regression test for https://github.com/pylint-dev/pylint/issues/10821
# Circular MRO inference caused RecursionError crash when a class inherits
# from a re-imported module member and patches it back conditionally.
from pdb import Pdb as StdlibPdb

class Pdb(StdlibPdb):  # [inconsistent-mro]
    ...

class PatchedPdb(Pdb):  # [inconsistent-mro]
    ...

if __name__ == '__main__':
    import pdb
    pdb.Pdb = PatchedPdb
    pdb.main()

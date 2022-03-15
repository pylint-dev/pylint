"""Tests for undefined-variable related to typing"""
# pylint: disable=invalid-name, import-error

# Ensure attribute lookups in type comments are accounted for.
# Reported in https://github.com/PyCQA/pylint/issues/4603

import foo
from foo import Bar, Boo

a = ...  # type: foo.Bar
b = ...  # type: foo.Bar[Boo]
c = ...  # type: Bar.Boo

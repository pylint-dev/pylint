"""Test for mypy extension package import crash regression.

This reproduces the crash described in issue #10223 where importing
mypy modules with --extension-pkg-allow-list=mypy caused an AttributeError
crash due to mypyc-compiled objects not having __dict__ attributes.

The fix ensures this generates an import-error message instead of crashing.
"""
# pylint: disable=unused-import

# This should not crash when using --extension-pkg-allow-list=mypy
import mypy.build  # [import-error]
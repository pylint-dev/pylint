"""Test for mypy extension package import crash regression."""
# pylint: disable=unused-import

# This should not crash when using --extension-pkg-allow-list=mypy
import mypy.build  # [import-error]
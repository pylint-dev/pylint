"""Regression test for https://github.com/PyCQA/pylint/issues/4692."""
# pylint: disable=magic-number

# We can't use click like in the issue because the crash
# does not appear if click is installed (astroid can analyse it)
import notclick  # [import-error]


for name, item in notclick.__dict__.items():
    _ = isinstance(item, notclick.Command) and item != 'foo'

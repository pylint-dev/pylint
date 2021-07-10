"""Regression test for https://github.com/PyCQA/pylint/issues/4692."""

import click  # [import-error]


for name, item in click.__dict__.items():
    _ = isinstance(item, click.Command) and item != 'foo'

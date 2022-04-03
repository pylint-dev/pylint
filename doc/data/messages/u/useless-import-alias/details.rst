Known issue
-----------

If you prefer to use `from ... import ... as ...` because using
`__all__` in `__init__.py` give error from other linter like `mypy`.
Use `pylint` Message Control `pylint: disable=useless-import-alias`
before any imports.
`GiHub Issue #6006 <https://github.com/PyCQA/pylint/issues/6006>`_
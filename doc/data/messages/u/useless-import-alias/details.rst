Known issue
-----------

If you prefer to use "from-as" to explicitly reexport in API (`from fruit import orange as orange`)
instead of using `__all__` this message will be a false positive.

If that's the case use `pylint: disable=useless-import-alias` before your imports in your API files.
`False positive 'useless-import-alias' error for mypy-compatible explicit re-exports #6006 <https://github.com/PyCQA/pylint/issues/6006>`_

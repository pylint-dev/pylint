Known issue
-----------

If you prefer to use "from-as" to explicitly reexport in API (``from fruit import orange as orange``)
instead of using ``__all__`` this message will be a false positive.

Use ``--allow-reexport-from-package`` to allow explicit reexports by alias
in package ``__init__`` files.

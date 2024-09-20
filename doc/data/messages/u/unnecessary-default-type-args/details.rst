At the moment, this check only works for ``Generator`` and ``AsyncGenerator``.

Starting with Python 3.13, the ``SendType`` and ``ReturnType`` default to ``None``.
As such it's no longer necessary to specify them. The ``collections.abc`` variants
don't validate the number of type arguments. Therefore the defaults for these
can be used in earlier versions as well.

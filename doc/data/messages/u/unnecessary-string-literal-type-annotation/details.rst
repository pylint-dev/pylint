On Python 3.14 and later, annotations are always evaluated lazily.
As such, string-literal type annotations like ``"Foo"`` are no longer
required to avoid forward-reference issues and can be replaced by
the bare name, e.g. ``Foo``.

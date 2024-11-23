Using the shorthand syntax for union types is |recommended over the typing module|__. This is consistent with the broader recommendation to prefer built-in types over imports (for example, using ``list`` instead of the now-deprecated ``typing.List``).

``typing.Optional`` can also cause confusion in annotated function arguments, since an argument annotated as ``Optional`` is still a *required* argument when a default value is not set. Explicitly annotating such arguments with ``type | None`` makes the intention clear.

.. |recommended over the typing module| replace:: recommended over the ``typing`` module
__ https://docs.python.org/3/library/typing.html#typing.Union

Formatted string literals (f-strings) give a concise, consistent syntax
that can replace most use cases for the ``%`` formatting operator,
``str.format()`` and ``string.Template``.

F-strings also perform better than alternatives; see
`this tweet <https://twitter.com/raymondh/status/1205969258800275456>`_ for
a simple example.

When using the ``logging`` module, prefer lazy parameter passing
(``logging.debug("msg %s", arg)``) over f-strings, to avoid conflicting
with ``logging-fstring-interpolation``. See
`issue 5286 <https://github.com/pylint-dev/pylint/issues/5286>`_.

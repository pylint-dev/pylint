Formatted string literals (f-strings) give a concise, consistent syntax
that can replace most use cases for the ``%`` formatting operator,
``str.format()`` and ``string.Template``.

F-strings also perform better than alternatives; see
`this tweet <https://twitter.com/raymondh/status/1205969258800275456>`_ for
a simple example.

Inside ``logging`` calls, applying this message would trigger
``logging-fstring-interpolation`` instead. Passing the arguments to the
logger (``logging.debug("msg %s", arg)``) avoids both messages and lets
the logger skip formatting entirely when the record is filtered out by
level. This matters when the arguments have an expensive ``__str__`` or
``__repr__``. See `issue 5286
<https://github.com/pylint-dev/pylint/issues/5286>`_ for the discussion.

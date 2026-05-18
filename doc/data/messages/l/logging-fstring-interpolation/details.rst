This message permits to allow f-string in logging and still be warned of
``logging-format-interpolation``.

When ``consider-using-f-string`` is also enabled, use lazy parameter
passing (``logging.debug("msg %s", arg)``) which silences both. See
`issue 5286 <https://github.com/pylint-dev/pylint/issues/5286>`_.

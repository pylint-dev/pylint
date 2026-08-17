This message permits to allow f-string in logging and still be warned of
``logging-format-interpolation``.

When ``consider-using-f-string`` is also enabled, the two messages
conflict inside ``logging`` calls. Passing the arguments to the logger
(``logging.debug("msg %s", arg)``) avoids both and lets the logger skip
formatting entirely when the record is filtered out by level. This
matters when the arguments have an expensive ``__str__`` or
``__repr__``. See `issue 5286
<https://github.com/pylint-dev/pylint/issues/5286>`_ for the discussion.

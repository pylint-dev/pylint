The `Python data model documentation <https://docs.python.org/3/reference/datamodel.html#object.__exit__>`_
names the three arguments of ``__exit__`` and ``__aexit__`` ``exc_type``, ``exc_value`` and
``traceback``. Using these names everywhere makes context managers easier to read.

Arguments matching ``ignored-argument-names`` (for example ``_``) are not checked, and
signatures using ``*args`` or ``**kwargs`` are ignored.

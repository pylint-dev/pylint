If you rely on a pattern like:

.. sourcecode:: python

    if guarded():
        var = 1

    if guarded():
        print(var)  # emits possibly-used-before-assignment

you may be concerned that ``possibly-used-before-assignment`` is not totally useful
in this instance. However, consider that pylint, as a static analysis tool, does
not know if ``guarded()`` is deterministic or talks to
a database. (Likewise, for ``guarded`` instead of ``guarded()``, any other
part of your program may have changed its value in the meantime.)

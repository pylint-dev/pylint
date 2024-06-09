You can use ``assert_never`` to mark exhaustive choices:

.. sourcecode:: python

    from typing import assert_never

    def handle_date_suffix(suffix):
        if suffix == "d":
            ...
        elif suffix == "m":
            ...
        elif suffix == "y":
            ...
        else:
            assert_never(suffix)

    if suffix in "dmy":
        handle_date_suffix(suffix)

If you rely on a pattern like:

.. sourcecode:: python

    if guarded():
        var = 1

    if guarded() or other_condition:
        print(var)  # emits possibly-used-before-assignment

you may be concerned that ``possibly-used-before-assignment`` is not totally useful
in this instance. However, consider that pylint, as a static analysis tool, does
not know if ``guarded()`` is deterministic or talks to
a database. (Likewise, for ``guarded`` instead of ``guarded()``, any other
part of your program may have changed its value in the meantime.)

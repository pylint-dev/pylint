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

Or, instead of `assert_never()`, you can call a function with a return
annotation of `Never` or `NoReturn`. Unlike in the general case, where
by design pylint ignores type annotations and does its own static analysis,
here, pylint treats these special annotations like a disable comment.

Pylint currently allows repeating the same test like this, even though this
lets some error cases through, as pylint does not assess the intervening code:

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

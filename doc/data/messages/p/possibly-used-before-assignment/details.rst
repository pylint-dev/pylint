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

    # what if code here affects the result of guarded()?

    if guarded():
        print(var)

But this exception is limited to the repeating the exact same test.
This warns:

.. sourcecode:: python

    if guarded():
        var = 1

    if guarded() or other_condition:
        print(var)  # [possibly-used-before-assignment]

If you find this surprising, consider that pylint, as a static analysis
tool, does not know if ``guarded()`` is deterministic or talks to
a database. For variables (e.g. ``guarded`` versus ``guarded()``),
this is less of an issue, so in this case,
``possibly-used-before-assignment`` acts more like a future-proofing style
preference than an error, per se.

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

Pylint currently allows repeating the same test like this, even though this
lets some error cases through, as pylint does not assess the intervening code:

.. sourcecode:: python

    if guarded():
        var = 1

    # what if code here affects the reuslt of guarded()?

    if guarded():
        print(var)

But this exception is limited to the repeating the exact same test.
This warns:

.. sourcecode:: python

    if guarded():
        var = 1

    if guarded() or other_condition:
        print(var)

If you find this surprising, consider that pylint, as a static analysis
tool, does not know if ``guarded()`` is deterministic or talks to
a database. For constants (e.g. ``guarded`` versus ``guarded()``),
this is less of an issue, so in this case,
``possibly-used-before-assignment`` acts more like a future-proofing style
preference than an error, per se.

With a mutable default value, with each call the default value is modified, i.e.:

.. code-block:: python

    whats_on_the_telly() # ["property of the zoo"]
    whats_on_the_telly() # ["property of the zoo", "property of the zoo"]
    whats_on_the_telly() # ["property of the zoo", "property of the zoo", "property of the zoo"]

A function call used as a default value has the same problem: it is evaluated once, when the
function is defined, and not each time the function is called, so every call that omits the
argument shares its result (the same uuid, the same timestamp...):

.. code-block:: python

    def store(data, key=f"{uuid4()}.json"):  # the uuid never changes
        ...

Use ``None`` as the default and create the value inside the function body instead. Calls that
return an immutable value, such as ``tuple()`` or ``int("1")``, are allowed. Add other calls
that are safe or intentional (e.g. ``fastapi.Depends``) to the ``allowed-default-calls`` option.

With a mutable default value, with each call the default value is modified, i.e.:

.. code-block:: python

    whats_on_the_telly() # ["property of the zoo"]
    whats_on_the_telly() # ["property of the zoo", "property of the zoo"]
    whats_on_the_telly() # ["property of the zoo", "property of the zoo", "property of the zoo"]

Use ``global`` when a function needs to rebind a module-level name. Omit the
declaration when the function only changes items in the object that the name
already refers to. For example, this function updates the module-level list:

.. code-block:: python

    prices = [10, 20]


    def update_price(index, price):
        prices[index] = price

An assignment such as ``prices = [11, 20]`` inside the function binds the name
locally by default. Declare ``global prices`` if that assignment is meant to
replace the module-level list.

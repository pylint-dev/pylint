If you do mean to compare the callable itself, for example to check which function
was passed as an argument, use ``is`` instead of ``==``. Functions are only ever
equal to themselves, so ``is`` gives the same result, states the intent, and is not
reported by this message:

.. code-block:: python

    def describe(callback):
        if callback is print:
            return "prints its arguments"
        return "does something else"

Bound methods are the exception: accessing a method on an instance creates a new
bound method object each time, so ``obj.method is obj.method`` is ``False``. Compare
the underlying functions instead, for example ``callback.__func__ is MyClass.method``.

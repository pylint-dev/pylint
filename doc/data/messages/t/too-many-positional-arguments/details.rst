Positional arguments work well for cases where the the use cases are
self-evident, such as unittest's ``assertEqual(first, second, msg=None)``.
Comprehensibility suffers beyond a handful of arguments, though, so for
functions that take more inputs, require that additional arguments be
passed by *keyword only* by preceding them with ``*``:

.. code-block:: python

    def make_noise(self, volume, *, color=noise.PINK, debug=True):
        ...

This is an extension check because the typing advantage could be fixed.

Regarding performance, float("nan") and float("inf") are slower than their counterpart math.inf and math.nan by a factor of 4 after the initial import of math.

.. code-block:: python

    import math
    import timeit

    time_math_inf = timeit.timeit('math.nan', globals=globals(), number=10**8)
    print(f'math.nan: {time_math_inf:.2f} seconds')

    import timeit
    time_inf_str = timeit.timeit('float("nan")', number=10**8)
    print(f'float("nan"): {time_inf_str:.2f} seconds')

Result::

    math.nan: 1.24 seconds
    float("nan"): 5.15 seconds

But if we take the initial import into account it's worse.

.. code-block:: python

    import timeit

    time_math_inf = timeit.timeit('import math;math.nan', globals=globals(), number=10**8)
    print(f'math.nan: {time_math_inf:.2f} seconds')

    import timeit
    time_inf_str = timeit.timeit('float("nan")', number=10**8)
    print(f'float("nan"): {time_inf_str:.2f} seconds')

Result::

    math.nan: 9.08 seconds
    float("nan"): 5.33 seconds

So the decision depends on how and how often you need to use it and what matter to you.

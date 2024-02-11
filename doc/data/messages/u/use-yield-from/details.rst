:code:`yield from` can be thought of as removing the intermediary (your for loop) between the function caller and the
requested generator. This enables the caller to directly communicate with the generator (e.g. using :code:`send()`).
This communication is not possible when manually yielding each element one by one in a loop.

PEP 380 describes the possibility of adding optimizations specific to :code:`yield from`. It looks like they
have not been implemented as of the time of writing. Even without said optimizations, the following snippet shows
that :code:`yield from` is marginally faster.

.. code-block:: sh

  $ python3 -m timeit "def yield_from(): yield from range(100)" "for _ in yield_from(): pass"
  100000 loops, best of 5: 2.44 usec per loop
  $ python3 -m timeit "def yield_loop():" "    for item in range(100): yield item" "for _ in yield_loop(): pass"
  100000 loops, best of 5: 2.49 usec per loop

The fix removes the square brackets, so the list comprehension becomes a
generator: ``any([apple > 2 for apple in basket])`` becomes
``any(apple > 2 for apple in basket)``.

The fix is **unsafe**, it is only applied with ``--fix --unsafe-fixes``.
``any`` stops as soon as it finds a true value, and ``all`` as soon as it finds
a false one, so with a generator the remaining values are never computed. This
is why the generator is faster, but it changes what the code does when computing
a value has an effect. In the example above, ``randint`` is called ten times with
the list, and maybe only once with the generator. When ``basket`` is an
iterator, the generator also leaves the apples it did not need in ``basket``.

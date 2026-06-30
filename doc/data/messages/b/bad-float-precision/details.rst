Float literals lose their source value in three ways: overflow to
``math.inf`` (``1.5e500``), underflow to ``0.0`` (``1e-1000``), or
truncation when the literal has more significant digits than
``float64`` can store (~15). This check flags all three cases.

The suggestion list pairs the runtime-equivalent literal — ``math.inf``
or ``0.0`` for over/underflow, the float's ``repr`` for truncation —
with ``decimal.Decimal("...")`` so the source value is preserved when
the loss matters.

Notation form (scientific vs. engineering vs. underscore grouping) is a
separate concern handled by ``bad-number-notation``.

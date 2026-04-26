Added two related checks:

- ``bad-number-notation`` (``C0329``): notation form for numeric literals — scientific, engineering, and PEP 515 underscore grouping.
- ``bad-float-precision`` (``C0330``): float literals that float64 can't represent faithfully — overflow to ``math.inf``, underflow to ``0.0``, or precision loss when the source has more digits than ``str(float)`` round-trips.

Both checks can be enabled or disabled independently.

When the source literal already uses PEP 515 underscore grouping in the mantissa
(e.g. ``1.002_737_811_911_354_48``), the suggested replacement preserves that
grouping rather than flattening it into a wall of digits.  Mixed
exponent + underscore literals are still suggested in their unmixed forms
since pylint disallows the mix.

Added the ``suggest-mantissa-underscore`` option (default off): when enabled,
scientific / engineering / ``repr`` suggestions always group the mantissa with
underscores, even when the source literal didn't.

Refs #10425

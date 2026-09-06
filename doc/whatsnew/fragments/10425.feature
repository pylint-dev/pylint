Added three related checks for numeric literals:

- ``bad-integer-notation`` (``C0331``): a large integer that doesn't group its digits with
  PEP 515 underscores, or groups them the wrong way. On by default.
- ``bad-float-notation`` (``C0329``): notation form for float literals — scientific,
  engineering, and PEP 515 underscore grouping. **Off by default**: whether a big float
  reads better as ``2.5e7`` or ``25_000_000.0`` is a matter of taste, and reviewers
  disagree about it, so pylint waits until a project has picked a side.
- ``bad-float-precision`` (``C0332``): float literals that float64 can't represent
  faithfully — overflow to ``math.inf``, underflow to ``0.0``, or precision loss when the
  source has more digits than ``str(float)`` round-trips. On by default.

Splitting integers from floats is what the split is for: an integer can only be rewritten
with underscores, which is uncontroversial, while rewriting a float means choosing a
notation, which isn't. Each check can be enabled or disabled on its own.

Two options keep the float check from churning code that was already fine:

- ``float-notation-min-gain`` (default ``0``): how many characters a suggestion must save
  before a plain float is flagged. ``0`` always rewrites, for projects that want one
  consistent notation; ``1`` only rewrites when the result is actually shorter, which
  leaves ``299792458.0`` and ``5724535.74068625`` alone.
- ``allow-aligned-exponents`` (default ``yes``): leaves a float alone when another float in
  the same statement shares its exponent, so a measurement and its margin of error can be
  read on one scale (``1.3806488e-23`` alongside ``0.0000013e-23``).

When the source literal already uses PEP 515 underscore grouping in the mantissa
(e.g. ``1.002_737_811_911_354_48``), the suggested replacement preserves that
grouping rather than flattening it into a wall of digits.  Mixed
exponent + underscore literals are still suggested in their unmixed forms
since pylint disallows the mix.

Added the ``suggest-mantissa-underscore`` option (default off): when enabled,
scientific / engineering / ``repr`` suggestions always group the mantissa with
underscores, even when the source literal didn't.

Refs #10425

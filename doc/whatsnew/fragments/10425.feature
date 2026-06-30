Added two related checks:

- ``bad-number-notation`` (``C0329``): notation form for numeric literals — scientific, engineering, and PEP 515 underscore grouping.
- ``bad-float-precision`` (``C0330``): float literals that float64 can't represent faithfully — overflow to ``math.inf``, underflow to ``0.0``, or precision loss when the source has more digits than ``str(float)`` round-trips.

Both checks can be enabled or disabled independently.

Refs #10425

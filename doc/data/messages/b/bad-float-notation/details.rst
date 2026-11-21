This message is off by default. Whether a big float reads better as ``2.5e7`` or as
``25_000_000.0`` is a matter of taste, and reviewers genuinely disagree about it, so
pylint waits until your project has picked a side. Integer literals are a separate,
less contentious question, handled by ``bad-integer-notation``.

Five options tune this message:

- ``float-notation-style``: left empty (allow all three, the default),
  ``scientific``, ``engineering``, and/or ``underscore``
- ``float-notation-threshold`` (defaults to 1e6)
- ``float-notation-min-gain`` (defaults to 0): how many characters a suggestion has
  to save before a plain float is flagged. 0 always rewrites, for projects that want
  one consistent notation; 1 only rewrites when the result is actually shorter.
- ``allow-aligned-exponents`` (defaults to yes): leave a float alone when another
  float in the same statement shares its exponent, so a measurement and its margin
  of error can be read on the same scale.
- ``suggest-mantissa-underscore`` (defaults to no): always group the digits of a
  suggestion with underscores, even when the original literal did not.

This check covers notation form only. Float-precision concerns — overflow, underflow,
more digits than a float can remember — are handled by ``bad-float-precision``.

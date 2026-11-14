``integer-notation-threshold`` (defaults to 1000000) sets how big a whole number has
to get before it is expected to space out its digits. Underscores that land in the
wrong places are flagged whatever the size of the number, because misplaced groups
are a mistake rather than a style.

Some big numbers are easier to recognize without underscores, so they are left alone:

- A run of digits that climbs or falls one step at a time, like ``1234567``,
  ``1234567890`` or ``987654321``. You read its shape, not its size.
- Any number listed in ``ignored-integers``. Use it for the numbers your project knows
  by heart, like a favorite lucky number: ``ignored-integers=2147483647`` keeps
  ``2147483647``, ``-2147483647`` and ``0x7FFFFFFF`` as they are.

For a single line, ``# pylint: disable=bad-integer-notation`` works too.

Underscore grouping is the only suggestion offered here: a whole number cannot be
written in scientific or engineering notation without turning into a float. Floats
are covered by ``bad-float-notation`` instead.

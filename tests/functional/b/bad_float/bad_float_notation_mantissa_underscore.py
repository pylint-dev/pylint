# pylint: disable=missing-docstring,invalid-name

# Plain literal above threshold — no underscores in source, but the option
# forces grouping in the scientific / engineering mantissa suggestions.
big_plain = 12345678.9  # [bad-float-notation]

# Source already has underscores (non-standard grouping) — grouped suggestions
# come from the source-had-underscore path, identical with or without the option.
bad_grouping = 1_2_345_678.9  # [bad-float-notation]

# Mixed exponent + underscore — pylint flags the mix itself, so suggestions
# stay unmixed (no underscores in mantissa) regardless of the option.
mixed = 1.234_567e6  # [bad-float-notation]

# Precision loss case — repr() also gets grouped when the option is set.
high_precision = 3.14159265358979323846  # [bad-float-precision]

# A repr that keeps its exponent: the mantissa is regrouped either side
# of the 'e', and here the mantissa is a bare '1'.
precision_loss_exponent_repr = 1.0000000000000000001e30  # [bad-float-precision]

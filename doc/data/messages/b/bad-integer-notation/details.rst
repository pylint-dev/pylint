``integer-notation-threshold`` (defaults to 1000000) sets how big a whole number has
to get before it is expected to space out its digits. Underscores that land in the
wrong places are flagged whatever the size of the number, because misplaced groups
are a mistake rather than a style.

Underscore grouping is the only suggestion offered here: a whole number cannot be
written in scientific or engineering notation without turning into a float. Floats
are covered by ``bad-float-notation`` instead.

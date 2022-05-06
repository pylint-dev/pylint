# pylint: disable=missing-docstring, invalid-name
# pylint: disable=literal-comparison,comparison-with-itself, import-error, comparison-of-constants
"""Test detection of NaN value comparison."""
import numpy

x = 42
a = x is numpy.NaN  # [nan-comparison]
b = x == numpy.NaN  # [nan-comparison]
c = x == float("nan")  # [nan-comparison]
d = x is float("nan")  # [nan-comparison]
e = numpy.NaN == numpy.NaN  # [nan-comparison]
f = x is 1
g = 123 is "123"
h = numpy.NaN is not x  # [nan-comparison]
i = numpy.NaN != x  # [nan-comparison]

j = x != numpy.NaN  # [nan-comparison]
j1 = x != float("nan")  # [nan-comparison]
k = x is not numpy.NaN  # [nan-comparison]
assert x == numpy.NaN  # [nan-comparison]
assert x is not float("nan")  # [nan-comparison]
if x == numpy.NaN:  # [nan-comparison]
    pass
z = bool(x is numpy.NaN)  # [nan-comparison]

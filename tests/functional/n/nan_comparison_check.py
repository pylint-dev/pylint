# pylint: disable=missing-docstring, invalid-name
# pylint: disable=literal-comparison,comparison-with-itself, import-error, comparison-of-constants
"""Test detection of NaN value comparison."""
import decimal
import math
from decimal import Decimal
from math import nan

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

# NaN spellings other than 'numpy.NaN' and 'float("nan")'
m1 = x == math.nan  # [nan-comparison]
m2 = x is not math.nan  # [nan-comparison]
m3 = x != nan  # [nan-comparison]
n1 = x == numpy.nan  # [nan-comparison]
n2 = x == numpy.NAN  # [nan-comparison]
n3 = x is numpy.nan  # [nan-comparison]
d1 = x == Decimal("nan")  # [nan-comparison]
d2 = x != decimal.Decimal("NaN")  # [nan-comparison]

# A NaN hidden behind a module level constant is still a NaN
MY_NAN = math.nan
c1 = x == MY_NAN  # [nan-comparison]

# Infinity is not NaN: comparing against it is meaningful, so stay silent
o1 = x == math.inf
o2 = x != float("inf")
o3 = x is numpy.inf
o4 = x == -math.inf
o5 = x == math.pi
o6 = x == Decimal("1.5")
o7 = x == Decimal(x)

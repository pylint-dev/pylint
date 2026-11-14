"""Check arguments that are never meaningful as infinity or NaN."""
# pylint: disable=missing-function-docstring,missing-class-docstring
# pylint: disable=consider-using-with,expression-not-assigned

import cmath
import fractions
import math
import queue
import threading
import time
import unittest
from datetime import datetime, timedelta

# Tolerances: an infinite one matches everything, a NaN one matches nothing.
math.isclose(1, 2, rel_tol=math.inf)  # [nonsensical-float-arg]
math.isclose(1, 2, abs_tol=math.nan)  # [nonsensical-float-arg]
math.isclose(1, 2, rel_tol=float("inf"))  # [nonsensical-float-arg]
math.isclose(1, 2, rel_tol=float("nan"))  # [nonsensical-float-arg]
math.isclose(1, 2, rel_tol=-math.inf)  # [nonsensical-float-arg]
math.isclose(1, 2, rel_tol=1e999)  # [nonsensical-float-arg]
cmath.isclose(1, 2, abs_tol=math.inf)  # [nonsensical-float-arg]

# Timeouts are turned into a deadline, which infinity overflows.
time.sleep(math.inf)  # [nonsensical-float-arg]
threading.Event().wait(math.inf)  # [nonsensical-float-arg]
threading.Condition().wait(timeout=math.nan)  # [nonsensical-float-arg]
threading.Lock().acquire(True, math.inf)  # [nonsensical-float-arg]
queue.Queue().get(True, math.inf)  # [nonsensical-float-arg]
queue.Queue().put("apple", True, math.inf)  # [nonsensical-float-arg]

# Conversions to an integer, directly or through a date or a ratio.
int(math.inf)  # [nonsensical-float-arg]
math.floor(math.nan)  # [nonsensical-float-arg]
math.ceil(math.inf)  # [nonsensical-float-arg]
math.trunc(math.inf)  # [nonsensical-float-arg]
fractions.Fraction(math.inf)  # [nonsensical-float-arg]
timedelta(seconds=math.inf)  # [nonsensical-float-arg]
timedelta(0, math.nan)  # [nonsensical-float-arg]
datetime.fromtimestamp(math.inf)  # [nonsensical-float-arg]

# A name bound to infinity is followed too.
FOREVER = math.inf
time.sleep(FOREVER)  # [nonsensical-float-arg]


class BananaTest(unittest.TestCase):
    def test_almost(self):
        self.assertAlmostEqual(1, 2, delta=math.inf)  # [nonsensical-float-arg]
        self.assertNotAlmostEqual(1, 2, None, None, math.inf)  # [nonsensical-float-arg]


# Finite arguments are fine.
math.isclose(1, 2, rel_tol=0.1)
math.isclose(1, 2, abs_tol=0.0)
time.sleep(60)
threading.Event().wait(0.5)
queue.Queue().get(True, 1.5)
int(1.5)
timedelta(seconds=1)
datetime.fromtimestamp(0)

# Infinity is only a problem for the arguments that cannot use it.
math.isclose(math.inf, math.inf)
math.isnan(math.nan)
print(math.inf, float("nan"))
timedelta(seconds=1) * 2

# Omitting the timeout is how you wait forever.
threading.Event().wait()
queue.Queue().get()

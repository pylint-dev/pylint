# pylint: disable=missing-docstring
# https://github.com/pylint-dev/pylint/issues/4221

import random
o = object()
if random.choice([True, False]):
    o.count = None
"abc".count("a")

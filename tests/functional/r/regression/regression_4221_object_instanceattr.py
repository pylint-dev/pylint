# pylint: disable=missing-docstring
# https://github.com/pylint-dev/pylint/issues/4221

import random
O = object()
if random.choice([True, False]):
    O.count = None
"abc".count("a")

# Regression test for https://github.com/pylint-dev/pylint/issues/7240
# `no-member` was emitted for names used inside a comprehension in a branch
# that is unreachable on the current platform, while the same direct call
# outside a comprehension was correctly ignored.
"""No `no-member` inside comprehensions guarded by a platform check."""
# pylint: disable=unnecessary-comprehension
import sys

if sys.platform == "linux":
    import os

    print(os.getgroups())
    print([group for group in os.getgroups()])
    print({group for group in os.getgroups()})

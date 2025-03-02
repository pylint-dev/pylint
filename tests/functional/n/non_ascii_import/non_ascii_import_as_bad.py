"""import non ascii alias"""
import os.path as łos  # [non-ascii-module-import]


# Usage should not raise a second error
TEST = łos.join("a", "b")

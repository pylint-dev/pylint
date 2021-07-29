# pylint: disable=missing-docstring

import sys

breakpoint()  # [forgotten-debug-statement]
sys.breakpointhook()  # [forgotten-debug-statement]
b = breakpoint
b()  # [forgotten-debug-statement]
bsys = sys.breakpointhook
bsys()  # [forgotten-debug-statement]

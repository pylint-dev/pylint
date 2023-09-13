# pylint: disable=missing-docstring

import pdb
import sys

breakpoint()  # [forgotten-debug-statement]
sys.breakpointhook()  # [forgotten-debug-statement]
pdb.set_trace()  # [forgotten-debug-statement]
b = breakpoint
b()  # [forgotten-debug-statement]

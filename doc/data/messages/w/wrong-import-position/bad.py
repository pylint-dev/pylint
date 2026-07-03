import os

home = os.environ["HOME"]

import sys  # [wrong-import-position]

print(f"Home directory is {home}", file=sys.stderr)

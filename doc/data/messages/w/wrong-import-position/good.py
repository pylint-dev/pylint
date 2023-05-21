import os
import sys

home = os.environ["HOME"]
print(f"Home directory is {home}", file=sys.stderr)

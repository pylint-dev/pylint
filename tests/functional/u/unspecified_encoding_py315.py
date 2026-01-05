"""No warnings for using open() without specifying an encoding (Python 3.15+)."""

import io
from pathlib import Path

FILENAME = "foo.bar"

open(FILENAME)
open(FILENAME, encoding=None)
io.open(FILENAME)
io.open(FILENAME, encoding=None)

Path(FILENAME).open()
Path(FILENAME).open(encoding=None)
Path(FILENAME).read_text()
Path(FILENAME).read_text(encoding=None)
Path(FILENAME).write_text("string")
Path(FILENAME).write_text("string", encoding=None)


"""
Test that a constant parameter of `typing.Annotated` does not emit `unused-import`.
`typing.Annotated` was introduced in Python version 3.9
"""

from pathlib import Path  # [unused-import]
import typing as t


example: t.Annotated[str, "Path"] = "/foo/bar"

# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/pylint-dev/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/pylint-dev/pylint/blob/main/CONTRIBUTORS.txt

"""Regression test for https://github.com/pylint-dev/pylint/issues/8419

Path.read_text without encoding should trigger unspecified-encoding.

Fix landed before pylint 2.13 (oldest Python-3.12-compatible version).
"""

from pathlib import Path

text = Path("file.txt").read_text()  # [unspecified-encoding]
print(text)

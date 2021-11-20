"""Warnings for using open() without specifying an encoding"""
# pylint: disable=consider-using-with
import io
import locale
from pathlib import Path

FILENAME = "foo.bar"
open(FILENAME, "w", encoding="utf-8")
open(FILENAME, "wb")
open(FILENAME, "w+b")
open(FILENAME)  # [unspecified-encoding]
open(FILENAME, "wt")  # [unspecified-encoding]
open(FILENAME, "w+")  # [unspecified-encoding]
open(FILENAME, "w", encoding=None)  # [unspecified-encoding]
open(FILENAME, "r")  # [unspecified-encoding]

with open(FILENAME, encoding="utf8", errors="surrogateescape") as f:
    pass

LOCALE_ENCODING = locale.getlocale()[1]
with open(FILENAME, encoding=LOCALE_ENCODING) as f:
    pass

with open(FILENAME) as f:  # [unspecified-encoding]
    pass

with open(FILENAME, encoding=None) as f:  # [unspecified-encoding]
    pass

LOCALE_ENCODING = None
with open(FILENAME, encoding=LOCALE_ENCODING) as f:  # [unspecified-encoding]
    pass

io.open(FILENAME, "w+b")
io.open_code(FILENAME)
io.open(FILENAME)  # [unspecified-encoding]
io.open(FILENAME, "wt")  # [unspecified-encoding]
io.open(FILENAME, "w+")  # [unspecified-encoding]
io.open(FILENAME, "w", encoding=None)  # [unspecified-encoding]

with io.open(FILENAME, encoding="utf8", errors="surrogateescape") as f:
    pass

LOCALE_ENCODING = locale.getlocale()[1]
with io.open(FILENAME, encoding=LOCALE_ENCODING) as f:
    pass

with io.open(FILENAME) as f:  # [unspecified-encoding]
    pass

with io.open(FILENAME, encoding=None) as f:  # [unspecified-encoding]
    pass

LOCALE_ENCODING = None
with io.open(FILENAME, encoding=LOCALE_ENCODING) as f:  # [unspecified-encoding]
    pass

LOCALE_ENCODING = locale.getlocale()[1]
Path(FILENAME).read_text(encoding=LOCALE_ENCODING)
Path(FILENAME).read_text(encoding="utf8")
Path(FILENAME).read_text("utf8")

LOCALE_ENCODING = None
Path(FILENAME).read_text()  # [unspecified-encoding]
Path(FILENAME).read_text(encoding=None)  # [unspecified-encoding]
Path(FILENAME).read_text(encoding=LOCALE_ENCODING)  # [unspecified-encoding]

LOCALE_ENCODING = locale.getlocale()[1]
Path(FILENAME).write_text("string", encoding=LOCALE_ENCODING)
Path(FILENAME).write_text("string", encoding="utf8")

LOCALE_ENCODING = None
Path(FILENAME).write_text("string")  # [unspecified-encoding]
Path(FILENAME).write_text("string", encoding=None)  # [unspecified-encoding]
Path(FILENAME).write_text("string", encoding=LOCALE_ENCODING)  # [unspecified-encoding]

LOCALE_ENCODING = locale.getlocale()[1]
Path(FILENAME).open("w+b")
Path(FILENAME).open()  # [unspecified-encoding]
Path(FILENAME).open("wt")  # [unspecified-encoding]
Path(FILENAME).open("w+")  # [unspecified-encoding]
Path(FILENAME).open("w", encoding=None)  # [unspecified-encoding]
Path(FILENAME).open("w", encoding=LOCALE_ENCODING)

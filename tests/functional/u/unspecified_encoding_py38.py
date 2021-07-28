"""Warnings for using open() without specifying an encoding"""
# pylint: disable=consider-using-with
import io
import locale

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

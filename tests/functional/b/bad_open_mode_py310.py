"""Before Python 3.11, open() accepted the "U" mode alongside reading."""
# pylint: disable=consider-using-with

NAME = "foo.bar"
open(NAME, "+rUb")
open(NAME, "Ut", encoding="utf-8")
open(NAME, "Ubr")
open(NAME, "Ua", encoding="utf-8")  # [bad-open-mode]
open(NAME, "Uw", encoding="utf-8")  # [bad-open-mode]

"""Warnings for using open() with an invalid mode string."""
# pylint: disable=consider-using-with

NAME = "foo.bar"
open(NAME, "wb")
open(NAME, "w", encoding="utf-8")
open(NAME, "rb")
open(NAME, "x", encoding="utf-8")
open(NAME, "br")
open(NAME, "+r", encoding="utf-8")
open(NAME, "xb")
open(NAME, "rwx", encoding="utf-8")  # [bad-open-mode]
open(NAME, "rr", encoding="utf-8")  # [bad-open-mode]
open(NAME, "+", encoding="utf-8")  # [bad-open-mode]
open(NAME, "xw", encoding="utf-8")  # [bad-open-mode]
open(NAME, "ab+")
open(NAME, "a+b")
open(NAME, "+ab")
open(NAME, "+rUb")
open(NAME, "x+b")
open(NAME, "Ua", encoding="utf-8")  # [bad-open-mode]
open(NAME, "Ur++", encoding="utf-8")  # [bad-open-mode]
open(NAME, "Ut", encoding="utf-8")
open(NAME, "Ubr")

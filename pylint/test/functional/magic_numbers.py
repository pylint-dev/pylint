"""Tests for magic numbers being used instead of predefined constants"""
import os
import re


def re_funcs():
    rgx = re.compile("pattern", 16)  # [magic-number-used]
    return rgx


def errno():
    try:
        os.mkdir('x')
    except OSError as exc:
        if exc.errno != 17:  # [magic-number-used]
            raise

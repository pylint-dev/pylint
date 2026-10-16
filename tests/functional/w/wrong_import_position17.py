"""Checks import position rule for for/while blocks."""
# pylint: disable=unused-import

import os

for _ in []:
    pass

import sys  # [wrong-import-position]

while False:
    pass

import logging  # [wrong-import-position]

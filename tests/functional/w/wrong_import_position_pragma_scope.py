"""Test wrong-import-position pragma scoping."""
# pylint: disable=unused-import,using-constant-test,import-error,unspecified-encoding

import os
import sys

CONSTANT_A = False  # pylint: disable=wrong-import-position
import time

CONSTANT_B = True
import logging  # [wrong-import-position]

CONSTANT_C = 42
import json  # pylint: disable=wrong-import-position

CONSTANT_D = "test"  # pylint: disable=wrong-import-position
import csv

try:
    import xml
except ImportError:
    pass

import pathlib  # [wrong-import-position]

if True:
    import random

import typing  # [wrong-import-position]

for _ in []:
    import html

import calendar  # [wrong-import-position]

while False:
    import decimal

import fractions  # [wrong-import-position]

with open(__file__):
    import gc

import hashlib  # [wrong-import-position]

match os.name:
    case "nt":
        import winreg

import base64  # [wrong-import-position]

try:  # pylint: disable=wrong-import-position
    import abc
except ImportError:
    pass

import collections

CONSTANT_E = 123
import re  # [wrong-import-position]

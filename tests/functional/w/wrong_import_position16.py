"""Checks import position rule with async def"""
# pylint: disable=unused-import,missing-function-docstring
async def async_func():
    pass
import os  # [wrong-import-position]

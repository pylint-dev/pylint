# pylint: disable=missing-function-docstring
"""Test async context manager used with regular 'with'."""

from contextlib import asynccontextmanager


@asynccontextmanager
async def async_cm():
    yield


with async_cm():  # [async-context-manager-with-regular-with]
    pass

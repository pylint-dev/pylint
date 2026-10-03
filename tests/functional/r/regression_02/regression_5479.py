"""Test for a regression on slots and annotated assignments.
Reported in https://github.com/pylint-dev/pylint/issues/5479
"""
# pylint: disable=too-few-public-methods, unused-private-member, missing-class-docstring, missing-function-docstring, declare-non-slot

from __future__ import annotations

import asyncio


class Connector:
    __slots__ = ("_Connector__reader", "_Connector__writer")

    __reader: asyncio.StreamReader
    __writer: asyncio.StreamWriter

    def __init__(self) -> None:
        raise TypeError("Use connect() instead")

    @classmethod
    async def connect(cls, socket: str) -> Connector:
        self = cls.__new__(cls)
        self.__reader, self.__writer = await asyncio.open_unix_connection(socket)
        return self


async def main():
    conn = await Connector.connect("/tmp/mysocket")  # [unused-variable]


asyncio.run(main())

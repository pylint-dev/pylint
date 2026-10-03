from collections.abc import AsyncGenerator, Generator

a1: AsyncGenerator[int, None]  # [unnecessary-default-type-args]
b1: Generator[int, None, None]  # [unnecessary-default-type-args]

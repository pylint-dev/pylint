"""Synchronous overrides can return a coroutine without awaiting it (#9745)."""
# pylint: disable=missing-docstring,too-few-public-methods
from asyncio import sleep
from typing import Any, Awaitable, Coroutine


class AsyncBase:
    async def run(self) -> None:
        pass


class ReturnsAwaitable(AsyncBase):
    def run(self) -> Awaitable[None]:
        return sleep(0)


class ReturnsCoroutine(AsyncBase):
    def run(self) -> Coroutine[Any, Any, None]:
        return sleep(0)


class Unannotated(AsyncBase):
    def run(self):
        return sleep(0)


class CallsMethod(AsyncBase):
    def run(self):
        return super().run()


class AsyncOverride(ReturnsCoroutine):
    async def run(self) -> None:
        pass


class MultipleReturns(AsyncBase):
    def run(self):
        if self:
            return sleep(0)
        return sleep(1)


class MixedReturns(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        if self:
            return None
        return sleep(0)


class BareReturn(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        if self:
            return
        return sleep(0)


class FallsThrough(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        if self:
            return sleep(0)


class NestedReturn(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        def inner():
            return None
        inner()


async def async_generator():
    yield 0


class ReturnsAsyncGenerator(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        return async_generator()


class IsGenerator(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        yield 0
        return sleep(0)


def synchronous():
    return None


class ReturnsSynchronousCall(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        return synchronous()


class UnknownCall(AsyncBase):
    def run(self):  # [invalid-overridden-method]
        return self.unknown()  # pylint: disable=no-member


class NestedFunction(AsyncBase):
    def run(self):
        def inner():
            return None
        inner()
        return sleep(0)

"""A method of a Protocol only declares what implementations return, so assigning
its result is not ``assignment-from-no-return``.

https://github.com/pylint-dev/pylint/issues/9080
"""
# pylint: disable=too-few-public-methods
from dataclasses import dataclass
from typing import Protocol


class Greeter(Protocol):
    """A protocol"""

    def greet(self) -> str:
        """Return a greeting"""
        ...

    def wave(self) -> str:
        """Return a wave, with a docstring as the only body"""


@dataclass
class Host:
    """Uses a Greeter"""

    greeter: Greeter

    def welcome(self):
        """The protocol's methods are not checked"""
        message = self.greeter.greet()
        wave = self.greeter.wave()
        return message, wave


class SilentGreeter(Greeter):
    """Implements the protocol without returning anything"""

    def greet(self):
        """No return"""
        print("hello")


def welcome_silently():
    """An implementation is still checked"""
    message = SilentGreeter().greet()  # [assignment-from-no-return]
    return message

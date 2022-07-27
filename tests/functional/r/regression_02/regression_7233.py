"""Regression test for https://github.com/PyCQA/pylint/issues/7233"""

# pylint: disable=missing-docstring

from dataclasses import dataclass


class MyHelloError(RuntimeError):
    @property
    def detail(self):
        return self.args[0]


@dataclass
class ErrorInfo:
    errorcode: int


try:
    raise MyHelloError(ErrorInfo(1234))
except MyHelloError as exc:
    print(exc.detail.errorcode)

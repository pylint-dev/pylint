"""Tests annotated Enum values (issue #11413)."""

# pylint: disable=missing-docstring,too-few-public-methods
import dataclasses
import datetime
import enum
from collections.abc import Callable


@dataclasses.dataclass(frozen=True)
class Payload:
    formatter: Callable[[datetime.date], str]


def format_date(value: datetime.date) -> str:
    return value.isoformat()


class FormatBase(enum.Enum):
    _value_: Payload

    def __call__(self, value: datetime.date) -> str:
        return self._value_.formatter(value)


class Format(FormatBase):
    _value_: Payload
    DEFAULT = Payload(formatter=format_date)


class AnnotatedFormat(enum.Enum):
    DEFAULT: Payload = Payload(formatter=format_date)


class FormatterMixin:
    formatter: Callable[[datetime.date], str]


class FormatWithMixin(FormatterMixin, enum.Enum):
    DEFAULT = Payload(formatter=format_date)


print(Format.DEFAULT(datetime.date(2026, 9, 13)))
print(AnnotatedFormat.DEFAULT.formatter(datetime.date(2026, 9, 13)))
print(FormatWithMixin.DEFAULT.formatter(datetime.date(2026, 9, 13)))
print(Format.DEFAULT.missing)  # [no-member]
print(AnnotatedFormat.DEFAULT.missing)  # [no-member]

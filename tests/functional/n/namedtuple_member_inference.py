"""Test namedtuple attributes.

Regression test for:
https://bitbucket.org/logilab/pylint/issue/93/pylint-crashes-on-namedtuple-attribute
"""
from collections import namedtuple
from typing import NamedTuple


Thing = namedtuple('Thing', ())

Fantastic = namedtuple('Fantastic', ['foo'])

def test():
    """Test member access in named tuples."""
    print(Thing.x)  # [no-member]
    fan = Fantastic(1)
    print(fan.foo)
    # Should not raise protected-access.
    fan2 = fan._replace(foo=2)
    print(fan2.foo)


class Lines(NamedTuple):
    """A typed named tuple that uses its generated API internally."""

    lines: list[str]

    def add_line(self, line: str) -> "Lines":
        """Return a copy with the line added."""
        return self._replace(lines=[*self.lines, line])

    def generated_members(self) -> tuple[object, ...]:
        """Exercise the other generated named tuple members."""
        return self._fields, self._field_defaults, self._asdict(), self._make([])

    def missing_member(self) -> None:
        """Keep checking members that are not part of the named tuple API."""
        print(self._missing)  # [no-member]

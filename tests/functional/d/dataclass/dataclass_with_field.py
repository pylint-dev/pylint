"""Regression test for https://github.com/pylint-dev/pylint/issues/4899"""

# pylint: disable=missing-docstring,too-few-public-methods

from dataclasses import field
from typing import List
from pydantic.dataclasses import dataclass # [import-error]


class Item:
    pass


@dataclass
class Case:
    """Case class (group Item)"""

    name: str
    irr: float = 0
    items: List[Item] = field(default_factory=lambda: [])

    def add_item(self, item: Item) -> None:
        """Add an item to the item list."""

        self.items.append(item)

    def find_item(self, description: str) -> Item:
        """Find an item by description"""

        return next(
            (item for item in self.items if item.description == description), None
        )

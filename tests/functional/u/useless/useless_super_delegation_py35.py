# pylint: disable=missing-docstring,too-few-public-methods,no-member,unused-argument, useless-object-inheritance

class NotUselessSuper(object):

    def not_passing_all_params(self, first, *args, second=None, **kwargs):
        return super().not_passing_all_params(*args, second, **kwargs)


class UselessSuper(object):

    def useless(self, first, *, second=None, **kwargs): # [useless-super-delegation]
        return super().useless(first, second=second, **kwargs)

# pylint: disable=wrong-import-position
import random
from typing import Any

class ReturnTypeAny:
    choices = ['a', 1, (2, 3)]

    def draw(self) -> Any:
        return random.choice(self.choices)

class ReturnTypeNarrowed(ReturnTypeAny):
    choices = [1, 2, 3]

    def draw(self) -> int:
        return super().draw()

class NoReturnType:
    choices = ['a', 1, (2, 3)]

    def draw(self):
        return random.choice(self.choices)

class ReturnTypeSpecified(NoReturnType):
    choices = ['a', 'b']

    def draw(self) -> str: # [useless-super-delegation]
        return super().draw()

class ReturnTypeSame(ReturnTypeAny):
    choices = ['a', 'b']

    def draw(self) -> Any: # [useless-super-delegation]
        return super().draw()

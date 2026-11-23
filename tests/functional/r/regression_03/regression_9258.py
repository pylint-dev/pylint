# Regression test for https://github.com/pylint-dev/pylint/issues/9258
# The `_HAS_DEFAULT_FACTORY` sentinel injected by the astroid dataclass brain
# leaked into module locals and was reported as an unused global variable.
"""No `unused-variable` for the dataclass `_HAS_DEFAULT_FACTORY` sentinel."""
import dataclasses


@dataclasses.dataclass
class Basket:
    """A basket of fruits."""

    fruits: list = dataclasses.field(default_factory=list)


Basket()

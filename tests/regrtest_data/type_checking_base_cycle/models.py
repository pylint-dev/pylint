"""The mixin's base is the subclass itself when type checking (see #9190)."""

# pylint: disable=too-few-public-methods

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from type_checking_base_cycle.pipe import Pipe

    _PipeDataRelatedMixinBase = Pipe
else:
    _PipeDataRelatedMixinBase = object


class PipeDataRelatedMixin(_PipeDataRelatedMixinBase):
    """Mixin whose base infers to its own subclass."""

    def get_statistic_aggregations(self: "Pipe", is_scrap):
        """Method with an annotated ``self``."""
        return is_scrap

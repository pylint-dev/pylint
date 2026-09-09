"""The subclass that the mixin's base resolves to."""

# pylint: disable=too-few-public-methods

from type_checking_base_cycle.models import PipeDataRelatedMixin


class Pipe(PipeDataRelatedMixin):
    """Subclass of the mixin."""

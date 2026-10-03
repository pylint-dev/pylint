from typing import final


@final
class PlatypusData:
    """General Platypus data."""

    average_length = 46
    average_body_temperature = 32


class FluorescentPlaytipus(PlatypusData):  # [subclassed-final-class]
    """Playtipus with fluorescent fur."""

from typing import final


@final
class PlatypusData:
    """General Platypus data."""

    average_length = 46
    average_body_temperature = 32


def print_average_length_platypus():
    output = f"The average length of a platypus is: {PlatypusData.average_length}cm"
    print(output)

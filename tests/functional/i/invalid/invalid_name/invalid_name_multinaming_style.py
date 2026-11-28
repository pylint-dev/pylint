"""Test for multi naming style."""


def UPPER():  # [invalid-name]
    """UPPER func that will generate invalid-name error."""


def lower():
    """lower func that satisfies the prevalent group `lower`."""


def anotherlower():
    """Another lower func that satisfies the prevalent group `lower`."""


class Record:
    """Two snake_case names determine the style, even if the third is written more often."""

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.fullName = ""  # [invalid-name]

    def update(self):
        """Use the first name."""
        self.fullName = self.first_name  # [invalid-name]

    def reset(self):
        """Use the last name."""
        self.fullName = self.last_name  # [invalid-name]


Record().fullName = "set by a caller"

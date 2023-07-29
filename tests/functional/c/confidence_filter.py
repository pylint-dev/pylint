"""Test for the confidence filter."""


class Client:
    """use provider class"""

    def __init__(self):
        self.set_later = 0

    def set_set_later(self, value):
        """set set_later attribute (introduce an inference ambiguity)"""
        self.set_later = value

print(Client().set_later.lower())
print(Client().foo)  # [no-member]

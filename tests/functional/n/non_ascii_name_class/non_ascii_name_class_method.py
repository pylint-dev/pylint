"""Non ASCII char in classmethod"""


class OkayClass:
    """We need a class docstring?"""

    def public(self):
        """Say something"""
        print(self)

    @classmethod
    def umlaut_ä(cls):  # [non-ascii-name]
        """do something"""
        return "ä"


# Usage should not raise a second error
OkayClass.umlaut_ä()

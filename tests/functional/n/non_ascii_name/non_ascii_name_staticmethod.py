"""static method with non ascii characters"""


class OkayClass:
    """Class Docstring"""

    def public(self):
        """Say it load"""

    @staticmethod
    def umlaut_ä():  # [non-ascii-name]
        """Say ä"""
        return "ä"


# Usage should not raise a second error
OkayClass.umlaut_ä()

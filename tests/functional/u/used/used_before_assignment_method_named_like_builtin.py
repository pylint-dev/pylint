"""Regression test for https://github.com/pylint-dev/pylint/issues/9115.

Class annotations that name a builtin, ``str`` or ``dict``, are not uses of a
method of the same name defined later in the class body.
"""

# pylint: disable=too-few-public-methods


class Message:
    """Attributes annotated with builtins, and methods named after them."""

    message_type: str
    payload: dict | str

    def dict(self):
        """Return the message as a dictionary."""
        return {"message_type": self.message_type, "payload": self.payload}

    def str(self):
        """Return the message as text."""
        return repr(self.dict())

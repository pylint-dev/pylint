"""https://www.logilab.org/ticket/6949."""


print(__dict__ is not None)  # [used-before-assignment]

__dict__ = {}

print(__dict__ is not None)

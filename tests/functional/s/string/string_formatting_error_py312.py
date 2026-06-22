"""PEP 701 (Python 3.12+) f-string features that the format-spec checker
must not misparse."""
# pylint: disable=missing-function-docstring

# Same-quote nesting: ``"`` inside the expression of a double-quoted
# f-string. The per-FormattedValue spec walker should not be confused by
# the inner string literal containing the f-string's outer quote char.
def f(name: str) -> str:
    return f"tags[{name.replace('[', '').replace(']', '').replace('"', '')}]"

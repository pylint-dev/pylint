"""Indirect tests that ExceptionGroup is inferred."""

try:
    ex_list = [ValueError("a"), ValueError("b"),  Exception("c")]
    raise ExceptionGroup("exceptions!", ex_list)
except* ValueError as exc:
    assert exc.exceptions
    assert exc.message

"""This does not crash in the functional tests, but it did when called directly."""

assert "\U00010000" == "\ud800\udc00"  # [comparison-of-constants]

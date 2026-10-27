"""Module that sets an attribute on ``demo``."""

import demo


def test_demo():
    """Set the attribute shadowed in ``demo.main``."""
    demo.some_redefined_variable = "something"
    demo.main()

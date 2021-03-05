"""Tests for redefining builtins."""

def function():
    """Allow some redefines."""
    dir = "path"  # allowed in config
    dict = "wrong"  # [redefined-builtin]
    print(dir, dict)

list = "not in globals" # [redefined-builtin]

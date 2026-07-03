"""Tests for redefining builtins."""

def function():
    """Allow some redefines."""
    dir = "path"  # allowed in config
    dict = "wrong"  # [redefined-builtin]
    print(dir, dict)

list = "not in globals" # [redefined-builtin]

def global_variable_redefine():
    """Shadow `len` using the `global` keyword."""
    global len
    len = 1  # [redefined-builtin]
